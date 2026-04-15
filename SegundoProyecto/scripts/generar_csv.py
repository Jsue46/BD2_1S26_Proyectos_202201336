"""Generate CSV datasets for Segundo Proyecto (Neo4j movie recommendation graph)."""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker


RANDOM_SEED = 20260126
COUNTS = {
    "usuarios": 500,
    "peliculas": 200,
    "actores": 100,
    "directores": 50,
    "generos": 15,
}

GENRE_NAMES = [
    "Action",
    "Adventure",
    "Comedy",
    "Crime",
    "Drama",
    "Fantasy",
    "Horror",
    "Mystery",
    "Romance",
    "SciFi",
    "Thriller",
    "Animation",
    "Documentary",
    "Family",
    "War",
]


def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 0)))


def write_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def build_nodes(fake: Faker, out_dir: Path) -> None:
    users = []
    for uid in range(1, COUNTS["usuarios"] + 1):
        users.append(
            {
                "user_id": uid,
                "nombre": fake.name(),
                "email": f"user{uid}@example.com",
                "edad": random.randint(18, 70),
                "pais": fake.country(),
            }
        )

    movies = []
    for pid in range(1, COUNTS["peliculas"] + 1):
        movies.append(
            {
                "pelicula_id": pid,
                "titulo": f"Movie {pid}",
                "anio_lanzamiento": random.randint(1980, 2025),
                "duracion": random.randint(75, 190),
                "sinopsis": fake.sentence(nb_words=18),
            }
        )

    genres = []
    for gid in range(1, COUNTS["generos"] + 1):
        genres.append(
            {
                "genero_id": gid,
                "nombre": GENRE_NAMES[gid - 1],
                "descripcion": f"Genre category: {GENRE_NAMES[gid - 1]}",
            }
        )

    actors = []
    for aid in range(1, COUNTS["actores"] + 1):
        actors.append(
            {
                "actor_id": aid,
                "nombre": fake.name(),
                "fecha_nacimiento": random_date(date(1950, 1, 1), date(2005, 12, 31)).isoformat(),
                "nacionalidad": fake.country(),
            }
        )

    directors = []
    for did in range(1, COUNTS["directores"] + 1):
        directors.append(
            {
                "director_id": did,
                "nombre": fake.name(),
                "fecha_nacimiento": random_date(date(1940, 1, 1), date(1998, 12, 31)).isoformat(),
                "nacionalidad": fake.country(),
            }
        )

    write_csv(out_dir / "usuarios.csv", ["user_id", "nombre", "email", "edad", "pais"], users)
    write_csv(
        out_dir / "peliculas.csv",
        ["pelicula_id", "titulo", "anio_lanzamiento", "duracion", "sinopsis"],
        movies,
    )
    write_csv(out_dir / "generos.csv", ["genero_id", "nombre", "descripcion"], genres)
    write_csv(
        out_dir / "actores.csv",
        ["actor_id", "nombre", "fecha_nacimiento", "nacionalidad"],
        actors,
    )
    write_csv(
        out_dir / "directores.csv",
        ["director_id", "nombre", "fecha_nacimiento", "nacionalidad"],
        directors,
    )


def build_relationships(fake: Faker, out_dir: Path) -> None:
    user_ids = list(range(1, COUNTS["usuarios"] + 1))
    movie_ids = list(range(1, COUNTS["peliculas"] + 1))
    genre_ids = list(range(1, COUNTS["generos"] + 1))
    actor_ids = list(range(1, COUNTS["actores"] + 1))
    director_ids = list(range(1, COUNTS["directores"] + 1))

    pertenece_a = []
    for pid in movie_ids:
        for gid in random.sample(genre_ids, random.randint(1, 3)):
            pertenece_a.append({"pelicula_id": pid, "genero_id": gid})

    dirigio = []
    for pid in movie_ids:
        did = random.choice(director_ids)
        dirigio.append({"director_id": did, "pelicula_id": pid})

    actuo_en = []
    used_roles = set()
    for pid in movie_ids:
        cast_size = random.randint(3, 8)
        selected_actors = random.sample(actor_ids, cast_size)
        for aid in selected_actors:
            role = f"Character_{random.randint(1, 1500)}"
            key = (aid, pid, role)
            while key in used_roles:
                role = f"Character_{random.randint(1, 1500)}"
                key = (aid, pid, role)
            used_roles.add(key)
            actuo_en.append({"actor_id": aid, "pelicula_id": pid, "personaje": role})

    es_amigo_de = []
    friend_edges = set()
    for uid in user_ids:
        candidates = [x for x in user_ids if x != uid]
        for fid in random.sample(candidates, k=random.randint(5, 12)):
            pair = tuple(sorted((uid, fid)))
            if pair not in friend_edges:
                friend_edges.add(pair)
                es_amigo_de.append(
                    {
                        "user_id": pair[0],
                        "friend_id": pair[1],
                        "fecha_amistad": random_date(date(2018, 1, 1), date(2026, 4, 1)).isoformat(),
                    }
                )

    le_gusta = []
    for uid in user_ids:
        for gid in random.sample(genre_ids, random.randint(2, 5)):
            le_gusta.append(
                {
                    "user_id": uid,
                    "genero_id": gid,
                    "nivel_interes": random.randint(1, 5),
                }
            )

    vio = []
    visto = set()
    for uid in user_ids:
        seen_count = random.randint(15, 35)
        for pid in random.sample(movie_ids, seen_count):
            key = (uid, pid)
            if key in visto:
                continue
            visto.add(key)
            vio.append(
                {
                    "user_id": uid,
                    "pelicula_id": pid,
                    "fecha_visualizacion": random_date(date(2022, 1, 1), date(2026, 4, 1)).isoformat(),
                    "completo": random.choice(["true", "false"]),
                }
            )

    califico = []
    rated = set()
    for uid in user_ids:
        rated_count = random.randint(8, 18)
        for pid in random.sample(movie_ids, rated_count):
            key = (uid, pid)
            if key in rated:
                continue
            rated.add(key)
            score = random.randint(1, 5)
            califico.append(
                {
                    "user_id": uid,
                    "pelicula_id": pid,
                    "puntuacion": score,
                    "fecha": random_date(date(2022, 1, 1), date(2026, 4, 1)).isoformat(),
                    "comentario": fake.sentence(nb_words=10),
                }
            )

    write_csv(out_dir / "pertenece_a.csv", ["pelicula_id", "genero_id"], pertenece_a)
    write_csv(out_dir / "dirigio.csv", ["director_id", "pelicula_id"], dirigio)
    write_csv(out_dir / "actuo_en.csv", ["actor_id", "pelicula_id", "personaje"], actuo_en)
    write_csv(out_dir / "es_amigo_de.csv", ["user_id", "friend_id", "fecha_amistad"], es_amigo_de)
    write_csv(out_dir / "le_gusta.csv", ["user_id", "genero_id", "nivel_interes"], le_gusta)
    write_csv(out_dir / "vio.csv", ["user_id", "pelicula_id", "fecha_visualizacion", "completo"], vio)
    write_csv(
        out_dir / "califico.csv",
        ["user_id", "pelicula_id", "puntuacion", "fecha", "comentario"],
        califico,
    )


def main() -> None:
    random.seed(RANDOM_SEED)
    fake = Faker()
    Faker.seed(RANDOM_SEED)

    base_dir = Path(__file__).resolve().parent.parent
    csv_dir = base_dir / "data" / "csv"

    build_nodes(fake, csv_dir)
    build_relationships(fake, csv_dir)

    print("CSV generation completed.")
    print(f"Output directory: {csv_dir}")


if __name__ == "__main__":
    main()
