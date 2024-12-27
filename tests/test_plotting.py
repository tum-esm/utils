import os
import platform
import tum_esm_utils


def test_plotting() -> None:
    figure_path = "/tmp/tum_esm_utils_plotting_test.png"
    if os.path.exists(figure_path):
        os.remove(figure_path)

    tum_esm_utils.plotting.apply_better_defaults(
        font_family="Roboto" if platform.system() == "Darwin" else None
    )

    with tum_esm_utils.plotting.create_figure("/tmp/tum_esm_utils_plotting_test.png") as fig:
        axis1 = tum_esm_utils.plotting.add_subplot(
            fig, (2, 1, 1), title="Test Plot", xlabel="X", ylabel="Y"
        )
        axis1.plot([1, 2, 3], [1, 2, 3])

        axis2 = tum_esm_utils.plotting.add_subplot(
            fig, (2, 1, 2), title="Test Plot 2", xlabel="X", ylabel="Y"
        )
        axis2.plot([1, 2, 3], [3, 2, 1])

        tum_esm_utils.plotting.add_colorpatch_legend(
            fig,
            handles=[
                ("Label 1", "red"),
                ("Label 2", "blue"),
                ("Label 3", (0.2, 0.5, 0.8)),
                ("Label 4", (0.2, 0.5, 0.8, 0.5)),
                ("Label 5", "#FF00FF"),
            ],
            ncols=3,
            location="upper right",
        )

    assert os.path.exists(figure_path)
    os.remove(figure_path)
