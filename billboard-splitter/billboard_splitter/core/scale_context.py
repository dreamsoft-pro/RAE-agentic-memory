
import logging
from typing import Tuple

# Stała do konwersji cm na punkty PostScript (1 pt = 1/72 cala)
CM_TO_PT = 72 / 2.54

class ScaleContext:
    def __init__(self, settings: dict):
        self.settings = settings
        self.sx, self.sy = self._calculate_scale_factors()

    def _calculate_scale_factors(self) -> Tuple[float, float]:
        scaling_settings = self.settings.get("scaling_settings", {})
        if scaling_settings.get('scale_non_uniform', False):
            sx = scaling_settings.get('scale_den_x', 10.0)
            sy = scaling_settings.get('scale_den_y', 10.0)
            logging.info(f"Using non-uniform scale: sx={sx}, sy={sy}")
        else:
            scale = scaling_settings.get('scale_den', 10.0)
            sx = sy = scale
            logging.info(f"Using uniform scale: {scale}")
        
        # Fallback for backward compatibility
        if 'scale_den' not in scaling_settings and 'scale_den_x' not in scaling_settings:
            logging.warning("Scale keys not found in scaling_settings, defaulting to 1:10.")
            return 10.0, 10.0
            
        return sx, sy

    def get_scale_factors(self) -> Tuple[float, float]:
        return self.sx, self.sy

    def cm_to_doc_x(self, cm: float) -> float:
        if self.sx <= 0:
            raise ValueError("Scale factor Sx must be positive.")
        return (cm * CM_TO_PT) / self.sx

    def cm_to_doc_y(self, cm: float) -> float:
        if self.sy <= 0:
            raise ValueError("Scale factor Sy must be positive.")
        return (cm * CM_TO_PT) / self.sy

    def get_output_dimensions_pt(self) -> Tuple[float, float]:
        orig_w_cm = self.settings.get('orig_w_cm', 0)
        orig_h_cm = self.settings.get('orig_h_cm', 0)

        # Check for overrides, but validate consistency
        out_width_cm_override = self.settings.get('out_width_cm')
        out_height_cm_override = self.settings.get('out_height_cm')

        calculated_w_cm = orig_w_cm * self.sx
        calculated_h_cm = orig_h_cm * self.sy
        
        final_w_cm = calculated_w_cm
        final_h_cm = calculated_h_cm

        # Validate if overrides are consistent with scale factors
        if out_width_cm_override is not None:
            if abs(out_width_cm_override - calculated_w_cm) > 0.1:
                logging.warning(
                    f"Overridden out_width_cm ({out_width_cm_override} cm) is inconsistent "
                    f"with original width and scale (expected {calculated_w_cm:.2f} cm). "
                    f"Using the value derived from scale factors for consistency."
                )
            else:
                final_w_cm = out_width_cm_override

        if out_height_cm_override is not None:
            if abs(out_height_cm_override - calculated_h_cm) > 0.1:
                logging.warning(
                    f"Overridden out_height_cm ({out_height_cm_override} cm) is inconsistent "
                    f"with original height and scale (expected {calculated_h_cm:.2f} cm). "
                    f"Using the value derived from scale factors for consistency."
                )
            else:
                final_h_cm = out_height_cm_override
        
        # The document dimensions are the scaled-down version
        doc_width_pt = (final_w_cm / self.sx) * CM_TO_PT
        doc_height_pt = (final_h_cm / self.sy) * CM_TO_PT

        return doc_width_pt, doc_height_pt

    def get_output_filename_suffix(self) -> str:
        if self.sx == self.sy:
            return f"_scale-1x{self.sx:.2f}".replace('.', 'p')
        else:
            return f"_scale-1x{self.sx:.2f}_1y{self.sy:.2f}".replace('.', 'p')

    def cm_to_pt_unscaled(self, cm: float) -> float:
        return cm * CM_TO_PT
