from mission_planning import route_planning
import math

class Rectangles:
    pku = {
        'min': (116.294, 39.980),
        'max': (116.315, 40.),
        'geo_ref': 'EPSG:4326'
    }
    china = {
        'min': (74., 10.),
        'max': (135., 54.),
        'geo_ref': 'EPSG:4326'
    }

def get_round(center, radius_m):
    get_coor_trans_mat = route_planning.get_coor_trans_mat
    one_point_coor_trans = route_planning.one_point_coor_trans

    delta_ = 0.001
    poly_ = [
        (center[0] - delta_, center[1] - delta_),
        (center[0] + delta_, center[1] - delta_),
        (center[0] + delta_, center[1] + delta_),
        (center[0] - delta_, center[1] + delta_),
    ]
    trans_mat, inv_trans_mat = get_coor_trans_mat(poly_, '4326', (1, 0))
    center_trans = one_point_coor_trans(center[0], center[1], trans_mat)
    vertex_num = 20
    round_points = []
    for i in range(vertex_num+1):
        deg_ = float(i) / vertex_num * math.pi * 2
        x = center_trans[0] + radius_m * math.cos(deg_)
        y = center_trans[1] + radius_m * math.sin(deg_)
        x, y = one_point_coor_trans(x, y, inv_trans_mat)
        round_points.append((x, y))
    return round_points


class Polygons:
    pku = {
        'vertex': [
            (116.294, 39.980),
            (116.294, 40.),
            (116.315, 40.),
            (116.315, 39.980),
            ],
        'geo_ref': 'EPSG:4326'
    }

    aoxiang = {
        'vertex': [(117.4033552216947, 39.55506045655302), (117.4037204603814, 39.55470122328266), (117.4045595510132, 39.55474387723272), (117.4051509740274, 39.5549278643604), (117.4054851268124, 39.55525167465338), (117.4040996881698, 39.55786627708388), (117.403513994072, 39.5583001463847), (117.4025999742523, 39.55828008312752), (117.4019728900704, 39.55779591763488)],
        'geo_ref': 'EPSG:4326'
    }
    
    aoxiang_big_str = '117.3605590691543,39.59989768599767,0 117.3802923947957,39.55037407769841,0 117.400304692556,39.55311648177857,0 117.4094263494858,39.55488375711138,0 117.3737676338526,39.60292985685081,0 117.3669659702266,39.60141789377526,0'

    aoxiang_big = {
        'vertex': [(float(x), float(y)) for x, y, z in [v_.split(',') for v_ in aoxiang_big_str.split(' ')]],
        'geo_ref': 'EPSG:4326'
    }

    aoxiang_huge_str = '117.3173535770051,39.58961458355139,0 117.3183409633097,39.58564658866697,0 117.3203489111637,39.5828354451159,0 117.3212996143876,39.58044269041655,0 117.3220529483965,39.57794618525018,0 117.3228034057614,39.5746488516974,0 117.3238632794922,39.57141777547724,0 117.3239319747626,39.57136990112147,0 117.3250977736941,39.56855023291215,0 117.3251756299774,39.56835224120852,0 117.3251788172445,39.56830218305193,0 117.3261056488623,39.56592415543531,0 117.3261143251794,39.56577365828429,0 117.3272105382559,39.56295907136821,0 117.3272139290381,39.56290928418952,0 117.3287910358297,39.56076802810411,0 117.3298187651148,39.55890375948819,0 117.3305285893377,39.55598898449748,0 117.3900082162722,39.5653052112481,0 117.3887704456965,39.56927080700545,0 117.3977046089638,39.57052639465099,0 117.3736624903865,39.60313218478183,0 117.3399175171437,39.59521376527411,0 117.3176439286077,39.59028173785151,0'

    aoxiang_huge = {
        'vertex': [(float(x), float(y)) for x, y, z in [v_.split(',') for v_ in aoxiang_huge_str.split(' ')]],
        'geo_ref': 'EPSG:4326'
    }

    aoxiang_fly_round = {
        'vertex': get_round((117.3816166666, 39.543980555556), 5000),
        'geo_ref': 'EPSG:4326'
    }