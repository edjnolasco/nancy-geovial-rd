from src.province_utils import canonical_province, normalize_text, province_key


def test_canonical_province_salcedo_maps_to_hermanas_mirabal():
    assert canonical_province("Salcedo") == "Hermanas Mirabal"


def test_canonical_province_la_estrelleta_maps_to_elias_pina():
    assert canonical_province("LaEstrelleta") == "Elías Piña"
    assert canonical_province("La Estrelleta") == "Elías Piña"


def test_canonical_province_el_seybo_maps_to_el_seibo():
    assert canonical_province("ElSeybo") == "El Seibo"
    assert canonical_province("El Seybo") == "El Seibo"


def test_canonical_province_compact_names_from_geojson():
    assert canonical_province("SanCristóbal") == "San Cristóbal"
    assert canonical_province("SantoDomingo") == "Santo Domingo"
    assert canonical_province("DistritoNacional") == "Distrito Nacional"
    assert canonical_province("LaVega") == "La Vega"


def test_canonical_province_historical_and_compact_aliases():
    assert canonical_province("HermanasMirabal") == "Hermanas Mirabal"
    assert canonical_province("Montecristi") == "Monte Cristi"


def test_canonical_province_preserves_known_canonical_names():
    assert canonical_province("Elías Piña") == "Elías Piña"
    assert canonical_province("Hermanas Mirabal") == "Hermanas Mirabal"
    assert canonical_province("San Pedro de Macorís") == "San Pedro de Macorís"


def test_normalize_text_removes_accents_and_normalizes_whitespace():
    assert normalize_text("  San   Cristóbal  ") == "san cristobal"
    assert normalize_text("Elías Piña") == "elias pina"
    assert normalize_text("Hermanas\tMirabal") == "hermanas mirabal"


def test_province_key_is_stable_for_canonical_and_alias_inputs():
    assert province_key("San Cristóbal") == "san_cristobal"
    assert province_key("SanCristóbal") == "san_cristobal"
    assert province_key("LaEstrelleta") == "elias_pina"
    assert province_key("Salcedo") == "hermanas_mirabal"


def test_unknown_province_returns_trimmed_original_name():
    assert canonical_province("Provincia Inventada") == "Provincia Inventada"
