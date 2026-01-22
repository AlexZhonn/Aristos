import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { ThemedView } from "../themed-view";

type StatsGridProps = {
  backgroundColor: string;
  borderColor: string;
  icon: string; // To handle the 💰 or 🥗 icons
  title: string;
  mainValue: string; // The big number (e.g. $0.00)
  mainLabel: string; // The label below (e.g. Spent Today)
  subValue: string; // The smaller number (e.g. $50.00)
  subLabel?: string; // Optional label (e.g. Remaining)
};

export default function StatsGrid({
  backgroundColor,
  borderColor,
  icon,
  title,
  mainValue,
  mainLabel,
  subValue,
  subLabel,
}: StatsGridProps) {
  return (
    <ThemedView
      style={[
        styles.grid,
        { backgroundColor: backgroundColor, borderColor: borderColor },
      ]}
    >
      {/* Header: Icon + Title */}
      <View style={styles.headerContainer}>
        <Text style={styles.icon}>{icon}</Text>
        <Text style={styles.title}>{title}</Text>
      </View>

      {/* Main Stat */}
      <View style={styles.mainStatContainer}>
        <Text style={styles.mainValue}>{mainValue}</Text>
        <Text style={styles.label}>{mainLabel}</Text>
      </View>

      {/* Sub Stat */}
      <View style={styles.subStatContainer}>
        <Text style={styles.subValue}>{subValue}</Text>
        {subLabel && <Text style={styles.label}>{subLabel}</Text>}
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  grid: {
    borderRadius: 16, // Slightly rounder to match design
    padding: 16, // Add padding so text isn't stuck to edges
    height: 200,
    width: "48%", // Use % so it fits 2 side-by-side perfectly
    borderWidth: 1,
    // We remove 'alignItems: center' so text stays left-aligned like the design
  },
  headerContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 16, // Space between header and big numbers
  },
  icon: {
    fontSize: 16,
    marginRight: 6,
  },
  title: {
    fontSize: 12,
    fontWeight: "700",
    color: "#B0B0B0", // Light grey for the title
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  mainStatContainer: {
    marginBottom: 16,
    paddingBottom: 10,
    borderBottomColor: "#737373",
    borderBottomWidth: 1,
  },
  mainValue: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#FFFFFF",
    marginBottom: 2,
  },
  subStatContainer: {
    // No specific style needed, just holds the bottom text
  },
  subValue: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#FFFFFF",
    marginBottom: 2,
  },
  label: {
    fontSize: 12,
    color: "#A0A0A0", // Dimmer text for labels
  },
});
