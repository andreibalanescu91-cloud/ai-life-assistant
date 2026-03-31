-- ─────────────────────────────────────────────────────────────────────────────
-- myPeppy — Supabase setup
-- Run this once in your Supabase project: SQL Editor → New query → Run
-- ─────────────────────────────────────────────────────────────────────────────

-- 1. Enable the pgvector extension (needed for semantic memory search)
create extension if not exists vector;


-- 2. Journal entries — one row per chat message, per user
create table if not exists journal_entries (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid not null references auth.users(id) on delete cascade,
    content     text not null,
    created_at  timestamptz not null default now()
);

-- Index for fast per-user timeline queries
create index if not exists idx_journal_user_date
    on journal_entries (user_id, created_at desc);

-- Row Level Security — users can only see their own entries
alter table journal_entries enable row level security;

create policy "Users see own journal entries"
    on journal_entries for all
    using (auth.uid() = user_id);


-- 3. Memories — one row per stored memory, with a 1024-dim embedding vector
create table if not exists memories (
    id            uuid primary key default gen_random_uuid(),
    user_id       uuid not null references auth.users(id) on delete cascade,
    content       text not null,
    content_hash  text not null,          -- MD5 of user_id:content for dedup
    embedding     vector(1024),           -- voyage-3 produces 1024-dim vectors
    created_at    timestamptz not null default now()
);

-- Unique constraint prevents duplicate memories per user
create unique index if not exists idx_memories_hash
    on memories (content_hash);

-- ivfflat index for fast approximate nearest-neighbour search
-- (rebuild this index after loading a large batch of initial data)
create index if not exists idx_memories_embedding
    on memories using ivfflat (embedding vector_cosine_ops)
    with (lists = 100);

-- Row Level Security
alter table memories enable row level security;

create policy "Users see own memories"
    on memories for all
    using (auth.uid() = user_id);


-- 4. RPC function for pgvector similarity search
--    Called by memory_db.retrieve_memory() as supabase.rpc("match_memories", {...})
create or replace function match_memories(
    query_embedding  vector(1024),
    match_user_id    uuid,
    match_count      int default 5
)
returns table (
    id       uuid,
    content  text,
    similarity float
)
language sql stable
as $$
    select
        id,
        content,
        1 - (embedding <=> query_embedding) as similarity
    from memories
    where user_id = match_user_id
    order by embedding <=> query_embedding
    limit match_count;
$$;


-- 5. Enable OAuth providers in Supabase Dashboard (cannot be done via SQL):
--    Authentication → Providers → enable Google, GitHub, Facebook
--    and paste in your OAuth app credentials for each.
--    See README.md for step-by-step instructions.
