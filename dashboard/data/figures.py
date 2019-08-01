def trucks_in_commune(trucks, communes):
    result = {
        'total_trucks': trucks.count(),
        'cat_b': 0,
        'cat_c': 0,
        'table': {
            'data': [],
            'columns': [
                {'data': 'commune'},
                {'data': 'total'},
                {'data': 'cat_b'},
                {'data': 'cat_c'}
            ],
            # Options
            'searching': False,
            'paging': False
        }
    }
    for com in communes:
        boundaries = com.boundaries
        #NOTE: IMPORTANT! As a placeholder we use the truck's last position. For the real deal this should use RT data or the position at a certain time
        trucks_here = trucks.filter(last_position__within=boundaries) 
        commune_data = {
            'commune': com.name,
            'total': trucks_here.count(),
            'cat_b': 0,
            'cat_c': 0
        }

        for th in trucks_here:
            truck_mam = th.weight_category
            if truck_mam > 3500:
                commune_data['cat_c'] += 1
            else:
                commune_data['cat_b'] += 1
        
        result['cat_b'] += commune_data['cat_b']
        result['cat_c'] += commune_data['cat_c']
        result['table']['data'].append(commune_data)
    
    return result
