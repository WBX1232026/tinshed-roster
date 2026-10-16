# Deployment

Owner: Li Qize (Technical Lead)
Related document: `docs/architecture.md`

## What gets deployed

A single Flask process serving the Tinshed Roster web app, with data kept in
one SQLite file. There is no separate database server and no external service.

## Option 1 — Docker (recommended)

The repository ships a `Dockerfile` and `docker-compose.yml`.

```bash
# Build and run
docker build -t tinshed-roster .
docker run -d -p 5000:5000 --name tinshed-roster tinshed-roster
# or, with compose:
docker compose up -d
# open http://localhost:5000
```

To stop and remove the container:

```bash
docker stop tinshed-roster && docker rm tinshed-roster
```

The image installs `requirements.txt`, copies the source, seeds the sample
season (when no database exists) and starts the app with
`python -m flask --app src.app run --host=0.0.0.0`.

## Option 2 — deploy script

`deploy/deploy.sh` does the same build/run steps in one command:

```bash
bash deploy/deploy.sh
# Builds the image, runs the container on port 5000
```

## Option 3 — bare Python

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python -m flask --app src.app run
```

## Seeding data

A fresh checkout has no database file. On first start the app loads the CSV
sample data automatically (`SEED_DATA=true` by default), or you can seed
explicitly:

```bash
python data/seed.py
# Seeded 10 volunteers and 1 productions (8 performances).
```

The seed writes `data/tinshed_roster.db` (see `DATABASE_URL`). Delete that file
to reset to the sample season.

## Verification checklist

- [ ] `pytest` passes (102 tests) — CI runs this on every push and PR
- [ ] Home page renders at `http://127.0.0.1:5000/`
- [ ] Roster gap view renders at `/roster/<performance_id>`
- [ ] Personal roster view renders at `/personal/<volunteer_id>`
- [ ] Restarting the app keeps previously created records (SQLite snapshot)

## Secrets handling

- The only configuration is `.env.example` (placeholders only).
- No real credentials, tokens or keys are committed to the repository.
- `DATABASE_URL` and `SEED_DATA` are the only environment variables; both have
  safe local defaults, so the app runs with no configuration at all.
