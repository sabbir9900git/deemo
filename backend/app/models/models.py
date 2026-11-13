from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class MarsLocation(Base):
    __tablename__ = "mars_locations"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(128), nullable=False, index=True)
    feature_type = Column(String(64), nullable=False)
    category = Column(String(64), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    diameter_km = Column(Float, nullable=True)
    elevation_m = Column(Float, nullable=True)
    zoom_tier = Column(String(32), nullable=False, index=True)  # zoom_out | medium_zoom | zoom_in
    quadrangle = Column(String(64), nullable=True)
    slope_deg = Column(Float, nullable=True)
    roughness_index = Column(Float, nullable=True)
    risk_level = Column(String(32), nullable=True)
    description = Column(Text, nullable=False)
    source_name = Column(String(128), nullable=False)
    source_url = Column(String(512), nullable=False)
    is_sample = Column(Boolean, default=False, nullable=False)

class DatasetSource(Base):
    __tablename__ = "dataset_sources"

    id = Column(String(64), primary_key=True, index=True)
    short_name = Column(String(64), nullable=False)
    title = Column(String(256), nullable=False)
    mission = Column(String(128), nullable=False)
    agency = Column(String(128), nullable=False)
    url = Column(String(512), nullable=False)
    portal_url = Column(String(512), nullable=True)
    data_type = Column(String(256), nullable=False)
    resolution = Column(String(128), nullable=False)
    coverage = Column(String(128), nullable=False)
    status = Column(String(128), nullable=False)
    citation = Column(Text, nullable=False)

class ScientificLayer(Base):
    __tablename__ = "scientific_layers"

    id = Column(String(64), primary_key=True, index=True)
    layer_number = Column(Integer, nullable=False)
    name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False)
    description = Column(Text, nullable=False)
    data_source = Column(String(256), nullable=False)
    instrument_mission = Column(String(256), nullable=False)
    observation_date = Column(String(128), nullable=True)
    units = Column(String(128), nullable=False)
    resolution = Column(String(128), nullable=True)
    availability_status = Column(String(128), nullable=False)
    is_derived = Column(Boolean, default=False, nullable=False)
    calculation_method = Column(Text, nullable=False)
    scientific_disclaimer = Column(Text, nullable=False)
    wmts_layer = Column(String(256), nullable=True)
    source_url = Column(String(512), nullable=False)

class MissionSite(Base):
    __tablename__ = "mission_sites"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    mission_name = Column(String(128), nullable=False)
    agency = Column(String(64), nullable=False)
    site_type = Column(String(64), nullable=False, index=True)
    status = Column(String(64), nullable=False)
    landing_date = Column(String(32), nullable=False)
    sols_operated = Column(Integer, nullable=True)
    mass_kg = Column(Float, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevation_m = Column(Float, nullable=True)
    region = Column(String(128), nullable=False)
    zoom_tier = Column(String(32), nullable=False)
    instruments = Column(Text, nullable=False)
    scientific_summary = Column(Text, nullable=False)
    source_url = Column(String(512), nullable=False)

class SavedRoute(Base):
    __tablename__ = "saved_routes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    profile = Column(String(32), nullable=False)  # shortest | lowest_risk | balanced
    start_name = Column(String(128), nullable=False)
    start_lat = Column(Float, nullable=False)
    start_lon = Column(Float, nullable=False)
    end_name = Column(String(128), nullable=False)
    end_lat = Column(Float, nullable=False)
    end_lon = Column(Float, nullable=False)
    total_distance_km = Column(Float, nullable=False)
    estimated_difficulty = Column(String(64), nullable=False)
    mean_risk_score = Column(Float, nullable=False)
    max_slope_deg = Column(Float, nullable=False)
    elevation_gain_m = Column(Float, nullable=False)
    is_provisional = Column(Boolean, default=False, nullable=False)
    is_sample = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)

    waypoints = relationship("RouteWaypoint", back_populates="route", cascade="all, delete-orphan")

class RouteWaypoint(Base):
    __tablename__ = "route_waypoints"

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("saved_routes.id"), nullable=False, index=True)
    sequence_index = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevation_m = Column(Float, nullable=False)
    slope_deg = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_class = Column(String(32), nullable=False)
    cumulative_km = Column(Float, nullable=False)

    route = relationship("SavedRoute", back_populates="waypoints")

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_key = Column(String(64), unique=True, nullable=False, index=True)
    default_view = Column(String(32), default="solar-system", nullable=False)
    active_layer_id = Column(String(64), default="base_map", nullable=False)
    scale_mode = Column(String(32), default="visual", nullable=False)
    show_labels = Column(Boolean, default=True, nullable=False)
    show_mission_sites = Column(Boolean, default=True, nullable=False)
    preferred_route_profile = Column(String(32), default="balanced", nullable=False)
