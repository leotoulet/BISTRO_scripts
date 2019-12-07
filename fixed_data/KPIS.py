#Defined frequently used KPIS

congestion_KPI = {
	"averageVehicleDelayPerPassengerTrip":0.333,
	"sustainability_GHG":0.333,
	"VMT":0.333
}

social_KPI = {
	"averageTravelCostBurden_Work":0.33,
	"busCrowding":0.33,
	"averageTravelCostBurden_Secondary":0.33
}

cost_burden_KPI = {
	"averageTravelCostBurden_Work":0.50,
	"averageTravelCostBurden_Secondary":0.50
}



VMT_KPI = {
	"VMT":1.0
}


Aggregate_1_KPI = {
	"averageVehicleDelayPerPassengerTrip":1*0.333/4,
	"sustainability_GHG":1*0.333/4,
	"VMT":1*0.333/4,
	"averageTravelCostBurden_Work":1*0.5/4,
	"averageTravelCostBurden_Secondary":1*0.5/4,
	"TollRevenue":-1.0/2
}

Aggregate_2_KPI = {
	"averageVehicleDelayPerPassengerTrip":1*0.333/3,
	"sustainability_GHG":1*0.333/3,
	"VMT":1*0.333/3,
	"averageTravelCostBurden_Work":1*0.5/3,
	"averageTravelCostBurden_Secondary":1*0.5/3,
	"TollRevenue":-1.0/3
}

Aggregate_3_KPI = {
	"averageVehicleDelayPerPassengerTrip":1*0.333/2,
	"sustainability_GHG":1*0.333/2,
	"VMT":1*0.333/2,
	"averageTravelCostBurden_Work":1*0.5/2,
	"averageTravelCostBurden_Secondary":1*0.5/4,
	"TollRevenue":-1.0/4
}


Aggregate_4_KPI = {
	"averageVehicleDelayPerPassengerTrip":1*0.333/4,
	"sustainability_GHG":1*0.333/4,
	"VMT":1*0.333/4,
	"averageTravelCostBurden_Work":1*0.5/2,
	"averageTravelCostBurden_Secondary":1*0.5/2,
	"TollRevenue":-1.0/4
}

Toll_Revenue_KPI = {
	"TollRevenue":-1.0
}

Avg_vehicule_delay_KPI = {
	"averageVehicleDelayPerPassengerTrip":1
}

Avg_cost_burden_work_KPI = {
	"averageTravelCostBurden_Work":1
}

Avg_cost_burden_secondary_KPI = {
	"averageTravelCostBurden_Secondary":1
}

Bus_crowding_KPI = {
	"busCrowding":1
}

ALL_KPIS = [Aggregate_1_KPI, Aggregate_2_KPI, Aggregate_3_KPI, Aggregate_4_KPI, VMT_KPI, cost_burden_KPI, congestion_KPI, social_KPI, TollRevenue_KPI, Avg_vehicule_delay_KPI]
ALL_KPIS += [Avg_cost_burden_work_KPI, Avg_cost_burden_secondary_KPI, Bus_crowding_KPI]

ALL_NAMES = ["Agg1", "Agg2", "Agg3", "Agg4", "VMT", "Cost Burden", "Congestion", "Social", "TR", "VHD"]
ALL_NAMES += ["CB_work", "CB_2ndary", "BC"]



"""
aggregate_KPI = {
	"averageVehicleDelayPerPassengerTrip":2*0.333/5,
	"sustainability_GHG":2*0.333/5,
	"VMT":2*0.333/5,
	"averageTravelCostBurden_Work":2*0.333/5,
	"busCrowding":2*0.333/5,
	"averageTravelCostBurden_Secondary":2*0.333/5,
	"TollRevenue":1.0/5
}

aggregate_KPI_2 = {
	"averageVehicleDelayPerPassengerTrip":2*0.333/5,
	"sustainability_GHG":2*0.333/5,
	"VMT":2*0.333/5,
	"averageTravelCostBurden_Work":2*0.5/5,
	"averageTravelCostBurden_Secondary":2*0.5/5,
	"TollRevenue":1.0/5
}

TollRevenue_KPI = {
	"TollRevenue":1.0
}
"""