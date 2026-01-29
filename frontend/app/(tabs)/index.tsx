import { Image } from "expo-image";
import { StyleSheet, RefreshControl, ActivityIndicator, View } from "react-native";
import { useState, useEffect } from "react";

import ParallaxScrollView from "@/components/parallax-scroll-view";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import StatsGrid from "@/components/ui/stats-grid";
import ChartCard from "@/components/ui/char-card";
import { analyticsAPI } from "@/services/api";

export default function HomeScreen() {
  const [todayData, setTodayData] = useState<any>(null);
  const [spendingTrends, setSpendingTrends] = useState<any>(null);
  const [calorieTrends, setCalorieTrends] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadDashboardData = async () => {
    try {
      const [today, spending, calories] = await Promise.all([
        analyticsAPI.today(),
        analyticsAPI.spending(14),
        analyticsAPI.calories(14),
      ]);
      
      setTodayData(today);
      setSpendingTrends(spending);
      setCalorieTrends(calories);
    } catch (error: any) {
      console.log("Dashboard data not available yet - backend not connected or not authenticated");
      // Set default/mock data for display
      setTodayData({
        spending: { spent_today: 0, remaining_budget: 50, budget: 50 },
        nutrition: { calories_today: 0, protein_today: 0 }
      });
      setSpendingTrends({ data_points: [] });
      setCalorieTrends({ data_points: [] });
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadDashboardData();
  };

  // Format data for charts
  const formatChartData = (dataPoints: any[]) => {
    return dataPoints.map((point, index) => ({
      value: point.amount || point.calories || 0,
      label: index % 3 === 0 ? point.label : undefined,
    }));
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#22C55E" />
        <ThemedText style={styles.loadingText}>Loading dashboard...</ThemedText>
      </View>
    );
  }

  const spendingData = spendingTrends ? formatChartData(spendingTrends.data_points) : [];
  const caloriesData = calorieTrends ? formatChartData(calorieTrends.data_points) : [];
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#A1CEDC", dark: "#1D3D47" }}
      headerImage={
        <Image
          source={require("@/assets/images/partial-react-logo.png")}
          style={styles.reactLogo}
        />
      }
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#22C55E" />
      }
    >
      <ThemedView style={styles.statsContainer}>
        <StatsGrid
          backgroundColor="#1A2B50"
          borderColor="#2A3C65"
          icon="💰"
          title="FINANCE"
          mainValue={`$${todayData?.spending?.spent_today?.toFixed(2) || "0.00"}`}
          mainLabel="Spent Today"
          subValue={`$${todayData?.spending?.remaining_budget?.toFixed(2) || "0.00"}`}
          subLabel="Remaining"
        />
        <StatsGrid
          backgroundColor="#1E3E2B"
          borderColor="#2E5E3B"
          icon="🥗"
          title="NUTRITION"
          mainValue={`${Math.round(todayData?.nutrition?.calories_today || 0)}`}
          mainLabel="Calories Today"
          subValue={`${todayData?.nutrition?.protein_today?.toFixed(1) || "0.0"}g`}
          subLabel="Protein Today"
        />
      </ThemedView>
      <ThemedView style={styles.graphSection}>
        <ThemedText type="subtitle" style={styles.sectionTitle}>
          Spending vs Calories (Last 14 Days)
        </ThemedText>

        <ChartCard
          title="Spending ($)"
          color="#3B82F6" // Blue
          data={spendingData}
        />

        <ChartCard
          title="Calories (kcal)"
          color="#22C55E" // Green
          data={caloriesData}
        />
      </ThemedView>
    </ParallaxScrollView>
  );
}
const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#000",
    gap: 16,
  },
  loadingText: {
    color: "#A1A1A1",
    fontSize: 16,
  },
  titleContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  statsContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 12,
    paddingHorizontal: 4,
  },
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: "absolute",
  },
  graphSection: {
    marginTop: 24,
    gap: 16,
  },
  sectionTitle: {
    marginBottom: 12,
    fontSize: 18,
    fontWeight: "bold",
  },
});
