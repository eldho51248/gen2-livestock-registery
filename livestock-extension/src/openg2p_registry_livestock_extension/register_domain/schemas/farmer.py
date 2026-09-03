from datetime import date

from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PGeoSchema,
    G2PRegisterHistorySchema,
    G2PGeoHistorySchema,
    G2PIntakeFormSchemaBase,
)


class G2PSchemaFarmer:

    farmer_id: str
    fayda_fan_id: str
    farmer_name: str
    first_name: str
    middle_name: str
    last_name: str
    gender: str
    date_of_birth: date
    mobile_number: str
    registration_date: date
    status: str


class G2PRegisterSchemaFarmer(G2PRegisterBaseSchema, G2PGeoSchema, G2PSchemaFarmer):
    """
    Schema for Farmer register.
    Inherits fields from G2PRegisterBaseSchema, G2PGeoSchema.
    Attributes inherited from G2PSchemaFarmer are specific to the Farmer domain.
    """


class G2PRegisterHistorySchemaFarmer(G2PRegisterHistorySchema, G2PGeoHistorySchema):
    """
    Schema for Farmer history.
    Inherits fields from G2PRegisterHistorySchema, G2PGeoHistorySchema.
    """


class G2PIntakeFormSchemaFarmer(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PGeoSchema, G2PSchemaFarmer):
    """
    Schema for Farmer intake form.
    Inherits fields from G2PRegisterBaseSchema, G2PGeoSchema.
    Attributes inherited from G2PSchemaFarmer are specific to the Farmer domain and are
    included in the intake form schema for data collection.
    """
