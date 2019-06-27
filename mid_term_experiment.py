import geo_polygons

def create_mid_term_experiment(rc):
    rc.gis_canvas.zoom_to_polygon(geo_polygons.Polygons.aoxiang_fly_round['vertex'], geo_polygons.Polygons.aoxiang_fly_round['geo_ref'])
    mm = rc.mission_manager
    mm.add_area('生态监测区（区域1）', [(117.3906, 39.5637), (117.4201, 39.5637), (117.4201, 39.5428), (117.3906, 39.5428)])
    mm.add_area('水域观测区（区域2）', [(117.4006, 39.5637), (117.4006, 39.5562), (117.4201, 39.5562), (117.4201, 39.5637)])
    mm.add_area('人、车目标跟踪观测区（区域3）', [(117.3906, 39.5543), (117.3906, 39.5505), (117.4100, 39.5505), (117.4100, 39.5543)])
    mm.add_fly_mission_to_area({
        'area_name': '生态监测区（区域1）',
        'mission_name': '植被覆盖提取生态观测任务',
        'aerocraft': '猛牛-轻小型固定翼无人机',
        'cameras': '多光谱相机',
        'ground_resolution_m': 0.1,
        'forward_overlap': 0.8,
        'sideway_overlap': 0.8,
        'fly_direction': 'longest_edge',
        'application': '大尺度生态应用(中期实验)',
        'aerocraft_num': 8,
        'board_region_name': '翱翔5km圆',
    })