/**
 * Welcome to the SQL editor
 * =========================
 */
CREATE OR REPLACE STREAM "DEFINATION_SQL_STREAM" (
    "DC_NOME" varchar(255),
    "TEMP" DECIMAL,
    "UMD" INTEGER
);

CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "DEFINATION_SQL_STREAM"
    SELECT STREAM
        "DC_NOME", (("TEMP" * 1.8) + 32), ("UMD" * 0.01)
    FROM "SOURCE_SQL_STREAM_001";

CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
            "DC_NOME"  varchar(255),
            "HEAT_INDEX" DOUBLE

);

CREATE OR REPLACE PUMP "OUT_PUMP" AS INSERT INTO "DESTINATION_SQL_STREAM"
    SELECT STREAM "DC_NOME",
        CASE
            WHEN (
                (1.1 * "TEMP") -10.3 + (0.047 * "UMD")
            ) < 80
            THEN (
                (1.1 * "TEMP") - 10.3 + (0.047 * "UMD")
            )
            WHEN (
                "TEMP" >= 80.0 AND "TEMP" <= 112.0 AND "UMD" <= 0.13
            )
            THEN (
                    (
                        - 42.379 + (2.04901523 * "TEMP")
                        + (10.14333127 * "UMD")
                        - (0.22475541 * "TEMP" * "UMD")
                        - (6.83783 * POWER(10, -3) * POWER("TEMP", 2))
                        - (5.481717 * POWER(10, -2) * POWER("UMD", 2))
                        + (1.22874 * POWER(10, -3) * POWER("TEMP", 2) * "UMD")
                        + (8.5282 * POWER(10, -4) * "TEMP" * POWER(10, 2))
                        - (1.99 * POWER(10, -6) * POWER("TEMP", 2) * POWER("UMD", 2))
                        )
                    - (
                        (3.25 - (0.25 * "UMD")) * POWER((17 - ABS("TEMP" - 95)) / 17, 0.5)
                    )
            )
            WHEN (
                "TEMP" >= 80.0 AND "TEMP" <= 87.0 AND "UMD" > 0.85
            )
            THEN (
                    ( - 42.379 + (2.04901523 * "TEMP")
                    + (10.14333127 * "UMD")
                    - (0.22475541 * "TEMP" * "UMD")
                    - (6.83783 * POWER(10, -3) * POWER("TEMP", 2))
                    - (5.481717 * POWER(10, -2) * POWER("UMD", 2))
                    + (1.22874 * POWER(10, -3) * POWER("TEMP", 2) * "UMD")
                    + (8.5282 * POWER(10, -4) * "TEMP" * POWER(10, 2))
                    - (1.99 * POWER(10, -6) * POWER("TEMP", 2) * POWER("UMD", 2))
                    )
                    + (
                        0.02
                        * ("UMD" - 85)
                        * (87 - "TEMP")
                    )
            )
        ELSE (
                (
                    - 42.379
                    + (2.04901523 * "TEMP")
                    + (10.14333127 * "UMD")
                    - (0.22475541 * "TEMP" * "UMD")
                    - (6.83783 * POWER(10, -3) * POWER("TEMP", 2))
                    - (5.481717 * POWER(10, -2) * POWER("UMD", 2))
                    + (1.22874 * POWER(10, -3) * POWER("TEMP", 2) * "UMD")
                    + (8.5282 * POWER(10, -4) * "TEMP" * POWER(10, 2))
                    - (1.99 * POWER(10, -6) * POWER("TEMP", 2) * POWER("UMD", 2))
                )
        )
        END
FROM "SOURCE_SQL_STREAM_001";