import { Image } from "expo-image";
import { Platform, StyleSheet } from "react-native";

import { HelloWave } from "@/components/hello-wave";
import ParallaxScrollView from "@/components/parallax-scroll-view";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
// import { Link } from "expo-router";
import StatsGrid from "@/components/ui/stats-grid";
import ChartCard from "@/components/ui/char-card";
import { Background } from "@react-navigation/elements";

export default function HomeScreen() {
  const spendingData = [
    { value: 0, label: "7" },
    { value: 0 },
    { value: 0 },
    { value: 2, label: "10" },
    { value: 0 },
    { value: 0 },
    { value: 1, label: "13" },
    { value: 0 },
    { value: 0 },
    { value: 0, label: "16" },
    { value: 0 },
    { value: 0 },
    { value: 26, label: "19" },
    { value: 2 }, // The big spike
  ];

  const caloriesData = [
    { value: 200, label: "7" },
    { value: 180 },
    { value: 190 },
    { value: 210, label: "10" },
    { value: 200 },
    { value: 220 },
    { value: 210, label: "13" },
    { value: 230 },
    { value: 255, label: "16" },
    { value: 240 },
    { value: 200 },
    { value: 180 },
    { value: 190, label: "19" },
    { value: 200 },
  ];
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#A1CEDC", dark: "#1D3D47" }}
      headerImage={
        <Image
          source={require("@/assets/images/partial-react-logo.png")}
          style={styles.reactLogo}
        />
      }
      style={{ BackgroundColor: "black" }}
    >
      <ThemedView style={styles.statsContainer}>
        <StatsGrid
          backgroundColor="#1A2B50" // Dark Blue
          borderColor="#2A3C65"
          icon="💰"
          title="FINANCE"
          mainValue="$0.00"
          mainLabel="Spent Today"
          subValue="$50.00"
          subLabel="Remaining"
        />
        <StatsGrid
          backgroundColor="#1E3E2B" // Dark Green
          borderColor="#2E5E3B"
          icon="🥗"
          title="NUTRITION"
          mainValue="0"
          mainLabel="Calories Today"
          subValue="0.0g"
          subLabel="Protein / 150g"
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
  titleContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  statsContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 12, // Adds a little gap between the two cards
    paddingHorizontal: 4, // Safety padding
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
