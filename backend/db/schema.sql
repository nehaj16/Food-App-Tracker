-- Food Tracker schema
-- ingredients: the canonical concept of a food ("chicken thighs"), deduped
-- inventory_items: each physical purchase, one row per purchase

CREATE TABLE IF NOT EXISTS ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    name TEXT NOT NULL UNIQUE,
    default_shelf_life_days INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS inventory_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    ingredient_id UUID NOT NULL REFERENCES ingredients (id),
    custom_name TEXT,
    quantity NUMERIC(10, 2),
    unit TEXT CHECK (
        unit IN (
            'g',
            'kg',
            'lb',
            'oz',
            'ml',
            'l',
            'fl_oz',
            'gal',
            'count',
            'dozen',
            'bag',
            'box',
            'can',
            'bottle',
            'pack'
        )
    ),
    location TEXT NOT NULL DEFAULT 'fridge',
    expiry_date DATE,
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_inventory_expiry ON inventory_items (expiry_date);

CREATE INDEX IF NOT EXISTS idx_inventory_is_deleted ON inventory_items (is_deleted);