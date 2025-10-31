"""
数据模型定义
Database Models Definition
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import json
from pathlib import Path

Base = declarative_base()

class Vehicle(Base):
    """车辆基本信息表"""
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String(17), unique=True, nullable=False, index=True, comment='车辆识别码')
    make = Column(String(50), nullable=False, comment='品牌')
    model = Column(String(100), nullable=False, comment='车型')
    year = Column(Integer, comment='年份')
    production_date = Column(DateTime, comment='生产日期')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    engine = relationship("Engine", back_populates="vehicle", uselist=False)
    transmission = relationship("Transmission", back_populates="vehicle", uselist=False)
    emission = relationship("Emission", back_populates="vehicle", uselist=False)
    parameters = relationship("VehicleParameter", back_populates="vehicle")
    test_reports = relationship("TestReport", back_populates="vehicle")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'vin': self.vin,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'production_date': self.production_date.isoformat() if self.production_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Engine(Base):
    """发动机信息表"""
    __tablename__ = 'engines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    engine_code = Column(String(50), nullable=False, comment='发动机型号')
    displacement = Column(Float, comment='排量(L)')
    power = Column(Float, comment='功率(kW)')
    torque = Column(Float, comment='扭矩(N·m)')
    fuel_type = Column(String(20), comment='燃料类型')
    aspiration = Column(String(20), comment='进气方式')
    cylinder_count = Column(Integer, comment='气缸数')
    configuration = Column(String(20), comment='气缸排列')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    vehicle = relationship("Vehicle", back_populates="engine")
    parameters = relationship("EngineParameter", back_populates="engine")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'engine_code': self.engine_code,
            'displacement': self.displacement,
            'power': self.power,
            'torque': self.torque,
            'fuel_type': self.fuel_type,
            'aspiration': self.aspiration,
            'cylinder_count': self.cylinder_count,
            'configuration': self.configuration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Transmission(Base):
    """变速箱信息表"""
    __tablename__ = 'transmissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    transmission_code = Column(String(50), nullable=False, comment='变速箱型号')
    transmission_type = Column(String(20), comment='变速箱类型')
    gear_count = Column(Integer, comment='档位数')
    drive_type = Column(String(20), comment='驱动方式')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    vehicle = relationship("Vehicle", back_populates="transmission")
    parameters = relationship("TransmissionParameter", back_populates="transmission")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'transmission_code': self.transmission_code,
            'transmission_type': self.transmission_type,
            'gear_count': self.gear_count,
            'drive_type': self.drive_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Emission(Base):
    """排放信息表"""
    __tablename__ = 'emissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    emission_standard = Column(String(20), nullable=False, comment='排放标准')
    co2_emission = Column(Float, comment='CO2排放(g/km)')
    fuel_consumption = Column(Float, comment='油耗(L/100km)')
    test_method = Column(String(50), comment='测试方法')
    test_date = Column(DateTime, comment='测试日期')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    vehicle = relationship("Vehicle", back_populates="emission")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'emission_standard': self.emission_standard,
            'co2_emission': self.co2_emission,
            'fuel_consumption': self.fuel_consumption,
            'test_method': self.test_method,
            'test_date': self.test_date.isoformat() if self.test_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class VehicleParameter(Base):
    """车辆参数表（动态参数）"""
    __tablename__ = 'vehicle_parameters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    parameter_name = Column(String(100), nullable=False, comment='参数名称')
    parameter_value = Column(Text, comment='参数值')
    parameter_unit = Column(String(20), comment='参数单位')
    parameter_category = Column(String(50), comment='参数类别')
    source_file = Column(String(255), comment='来源文件')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    vehicle = relationship("Vehicle", back_populates="parameters")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'parameter_name': self.parameter_name,
            'parameter_value': self.parameter_value,
            'parameter_unit': self.parameter_unit,
            'parameter_category': self.parameter_category,
            'source_file': self.source_file,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class EngineParameter(Base):
    """发动机参数表（动态参数）"""
    __tablename__ = 'engine_parameters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    engine_id = Column(Integer, ForeignKey('engines.id'), nullable=False)
    parameter_name = Column(String(100), nullable=False, comment='参数名称')
    parameter_value = Column(Text, comment='参数值')
    parameter_unit = Column(String(20), comment='参数单位')
    parameter_category = Column(String(50), comment='参数类别')
    source_file = Column(String(255), comment='来源文件')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    engine = relationship("Engine", back_populates="parameters")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'engine_id': self.engine_id,
            'parameter_name': self.parameter_name,
            'parameter_value': self.parameter_value,
            'parameter_unit': self.parameter_unit,
            'parameter_category': self.parameter_category,
            'source_file': self.source_file,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TransmissionParameter(Base):
    """变速箱参数表（动态参数）"""
    __tablename__ = 'transmission_parameters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transmission_id = Column(Integer, ForeignKey('transmissions.id'), nullable=False)
    parameter_name = Column(String(100), nullable=False, comment='参数名称')
    parameter_value = Column(Text, comment='参数值')
    parameter_unit = Column(String(20), comment='参数单位')
    parameter_category = Column(String(50), comment='参数类别')
    source_file = Column(String(255), comment='来源文件')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    transmission = relationship("Transmission", back_populates="parameters")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'transmission_id': self.transmission_id,
            'parameter_name': self.parameter_name,
            'parameter_value': self.parameter_value,
            'parameter_unit': self.parameter_unit,
            'parameter_category': self.parameter_category,
            'source_file': self.source_file,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TestReport(Base):
    """测试报告表"""
    __tablename__ = 'test_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    report_type = Column(String(50), nullable=False, comment='报告类型')
    test_date = Column(DateTime, nullable=False, comment='测试日期')
    test_result = Column(String(20), comment='测试结果')
    test_data = Column(Text, comment='测试数据(JSON格式)')
    report_file = Column(String(255), comment='报告文件路径')
    operator = Column(String(100), comment='操作员')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    vehicle = relationship("Vehicle", back_populates="test_reports")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'report_type': self.report_type,
            'test_date': self.test_date.isoformat() if self.test_date else None,
            'test_result': self.test_result,
            'test_data': json.loads(self.test_data) if self.test_data else None,
            'report_file': self.report_file,
            'operator': self.operator,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DataSource(Base):
    """数据源表"""
    __tablename__ = 'data_sources'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(255), nullable=False, comment='文件名')
    file_path = Column(String(500), nullable=False, comment='文件路径')
    file_type = Column(String(20), nullable=False, comment='文件类型')
    file_size = Column(Integer, comment='文件大小(字节)')
    processed = Column(String(20), default='pending', comment='处理状态')
    processed_date = Column(DateTime, comment='处理日期')
    error_message = Column(Text, comment='错误信息')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'processed': self.processed,
            'processed_date': self.processed_date.isoformat() if self.processed_date else None,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Template(Base):
    """报告模板表"""
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    template_name = Column(String(100), nullable=False, comment='模板名称')
    template_type = Column(String(50), nullable=False, comment='模板类型')
    template_file = Column(String(255), nullable=False, comment='模板文件路径')
    field_mapping = Column(Text, comment='字段映射(JSON格式)')
    description = Column(Text, comment='模板描述')
    is_active = Column(String(20), default='active', comment='是否激活')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'template_name': self.template_name,
            'template_type': self.template_type,
            'template_file': self.template_file,
            'field_mapping': json.loads(self.field_mapping) if self.field_mapping else None,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# 数据库初始化
def init_database(database_url=None):
    """初始化数据库"""
    if database_url is None:
        # 确保数据目录存在
        data_dir = Path(__file__).parent.parent.parent / 'data'
        data_dir.mkdir(exist_ok=True)
        db_path = data_dir / 'car_data.db'
        database_url = f'sqlite:///{db_path}'

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session(database_url=None):
    """获取数据库会话"""
    if database_url is None:
        # 确保数据目录存在
        data_dir = Path(__file__).parent.parent.parent / 'data'
        data_dir.mkdir(exist_ok=True)
        db_path = data_dir / 'car_data.db'
        database_url = f'sqlite:///{db_path}'

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()