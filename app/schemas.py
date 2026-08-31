from pydantic import BaseModel

class PredictionInput(BaseModel):
    wti_crude_high: float
    wti_crude_low: float
    wti_crude_open: float
    wti_crude_volume: float
    brent_crude_close: float
    brent_crude_high: float
    brent_crude_low: float
    brent_crude_open: float
    brent_crude_volume: float
    natural_gas_close: float
    natural_gas_high: float
    natural_gas_low: float
    natural_gas_open: float
    natural_gas_volume: float
    refinery_utilization_pct: float
    refinery_crude_inputs_kbd: float
    refinery_gross_inputs_kbd: float
    refinery_operable_capacity_kbd: float
    crude_oil_imports_kbd: float
    crude_oil_exports_kbd: float
    total_petroleum_product_imports_kbd: float
    total_petroleum_product_exports_kbd: float
    net_total_crude_and_product_imports_kbd: float


class PredictionOutput(BaseModel):
    wti_crude_close: float