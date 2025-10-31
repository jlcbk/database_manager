"""
数据库查询引擎
Database Query Engine
"""

import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .models import Vehicle, Engine, Transmission, Emission, VehicleParameter, init_database

logger = logging.getLogger(__name__)

class QueryEngine:
    """数据库查询引擎"""

    def __init__(self, database_url=None):
        self.engine = init_database(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """获取数据库会话"""
        return self.Session()

    def search_by_vin(self, vin: str) -> Dict[str, Any]:
        """通过VIN码查询完整信息"""
        session = self.get_session()
        try:
            # 查询车辆基本信息
            vehicle = session.query(Vehicle).filter(Vehicle.vin == vin).first()
            if not vehicle:
                return {}

            result = {
                'vehicle': vehicle.to_dict() if vehicle else None,
                'engine': None,
                'transmission': None,
                'emission': None,
                'parameters': []
            }

            # 查询发动机信息
            if vehicle.engine:
                result['engine'] = vehicle.engine.to_dict()

            # 查询变速箱信息
            if vehicle.transmission:
                result['transmission'] = vehicle.transmission.to_dict()

            # 查询排放信息
            if vehicle.emission:
                result['emission'] = vehicle.emission.to_dict()

            # 查询动态参数
            parameters = session.query(VehicleParameter).filter(
                VehicleParameter.vehicle_id == vehicle.id
            ).all()
            result['parameters'] = [p.to_dict() for p in parameters]

            return result

        except Exception as e:
            logger.error(f"查询VIN {vin} 时出错: {e}")
            return {}
        finally:
            session.close()

    def search_by_engine_code(self, engine_code: str) -> List[Dict[str, Any]]:
        """通过发动机型号查询相关车辆"""
        session = self.get_session()
        try:
            engines = session.query(Engine).filter(Engine.engine_code == engine_code).all()
            results = []

            for engine in engines:
                if engine.vehicle:
                    vehicle_data = self.search_by_vin(engine.vehicle.vin)
                    results.append(vehicle_data)

            return results

        except Exception as e:
            logger.error(f"查询发动机型号 {engine_code} 时出错: {e}")
            return []
        finally:
            session.close()

    def get_all_vehicles(self) -> List[Dict[str, Any]]:
        """获取所有车辆信息"""
        session = self.get_session()
        try:
            vehicles = session.query(Vehicle).all()
            return [vehicle.to_dict() for vehicle in vehicles]
        except Exception as e:
            logger.error(f"获取所有车辆信息时出错: {e}")
            return []
        finally:
            session.close()

    def add_vehicle(self, vehicle_data: Dict[str, Any]) -> bool:
        """添加车辆信息"""
        session = self.get_session()
        try:
            vehicle = Vehicle(
                vin=vehicle_data.get('vin'),
                make=vehicle_data.get('make'),
                model=vehicle_data.get('model'),
                year=vehicle_data.get('year'),
                production_date=vehicle_data.get('production_date')
            )

            session.add(vehicle)
            session.commit()
            logger.info(f"车辆信息添加成功: {vehicle_data.get('vin')}")
            return True

        except Exception as e:
            session.rollback()
            logger.error(f"添加车辆信息时出错: {e}")
            return False
        finally:
            session.close()