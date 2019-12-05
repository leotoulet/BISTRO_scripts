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

TollRevenue_KPI = {
	"TollRevenue":1.0
}

VMT_KPI = {
	"VMT":1.0
}

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

inverted_tolls_aggregate2_KPI = {
	"averageVehicleDelayPerPassengerTrip":1*0.333/4,
	"sustainability_GHG":1*0.333/4,
	"VMT":1*0.333/4,
	"averageTravelCostBurden_Work":1*0.5/4,
	"averageTravelCostBurden_Secondary":1*0.5/4,
	"TollRevenue":-1.0/2
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

ALL_KPIS = [inverted_tolls_aggregate2_KPI, aggregate_KPI, aggregate_KPI_2, VMT_KPI, cost_burden_KPI, congestion_KPI, social_KPI, TollRevenue_KPI, Avg_vehicule_delay_KPI]
ALL_KPIS += [Avg_cost_burden_work_KPI, Avg_cost_burden_secondary_KPI, Bus_crowding_KPI]

ALL_NAMES = ["Inverted_tolls_agg2", "Aggregate", "Aggregate_2", "VMT", "Cost Burden", "Congestion", "Social", "TR", "VHD"]
ALL_NAMES += ["CB_work", "CB_2ndary", "BC"]