import { StyleSheet, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router"; // Optional: for navigation

import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import ParallaxScrollView from "@/components/parallax-scroll-view";

export default function PantryScreen() {
  const router = useRouter();

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#D0D0D0", dark: "#1D3D47" }} // Matching theme
      headerImage={
        <Ionicons size={310} name="basket-outline" style={styles.headerImage} />
      }
    >
      <ThemedView style={styles.container}>
        {/* Header Section */}
        <View style={styles.titleContainer}>
          <ThemedText type="title">Virtual Pantry</ThemedText>
          <ThemedText style={styles.subtitle}>0 items in stock</ThemedText>
        </View>

        {/* Empty State Content */}
        <View style={styles.emptyStateContainer}>
          <Ionicons
            name="basket"
            size={80}
            color="#333"
            style={styles.emptyIcon}
          />
          <ThemedText type="subtitle" style={styles.emptyTitle}>
            Your pantry is empty
          </ThemedText>
          <ThemedText style={styles.emptySubtitle}>
            Scan receipts to add items
          </ThemedText>
        </View>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 16,
    // We use minHeight to ensure the empty state stays centered
    // even if the scrollview is short
    minHeight: 500,
  },
  headerImage: {
    color: "#666", // Subtle grey for the parallax background
    bottom: -90,
    left: -35,
    position: "absolute",
    opacity: 0.15,
  },
  titleContainer: {
    marginTop: 10,
    marginBottom: 40,
  },
  subtitle: {
    color: "#A1A1A1",
    fontSize: 16,
    marginTop: 4,
  },
  emptyStateContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 60, // Push it down a bit to center it visually
    gap: 12,
  },
  emptyIcon: {
    marginBottom: 8,
    opacity: 0.8,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: "bold",
  },
  emptySubtitle: {
    color: "#888",
    fontSize: 16,
  },
});
