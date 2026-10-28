from main import plot_probability_distribution


def test_probability_figure_is_vector_pdf(tmp_path):
    path = plot_probability_distribution(tmp_path / "p.pdf")
    assert path.read_bytes().startswith(b"%PDF")
