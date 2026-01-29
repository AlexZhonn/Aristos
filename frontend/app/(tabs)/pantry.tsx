import { StyleSheet, View, ScrollView, RefreshControl, ActivityIndicator, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
import { useState, useEffect } from "react";

import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import ParallaxScrollView from "@/components/parallax-scroll-view";
import IngredientCard from "@/components/ui/ingredient-card";
import { pantryAPI } from "@/services/api";

export default function PantryScreen() {
  const router = useRouter();
  const [pantryItems, setPantryItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState<string | null>(null);

  const loadPantry = async () => {
    try {
      const items = await pantryAPI.list(filter || undefined);
      setPantryItems(items);
    } catch (error: any) {
      console.error("Error loading pantry:", error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadPantry();
  }, [filter]);

  const onRefresh = () => {
    setRefreshing(true);
    loadPantry();
  };

  const handleConsume = async (itemId: string) => {
    try {
      await pantryAPI.consume(itemId);
      loadPantry(); // Reload
    } catch (error: any) {
      console.error("Error consuming item:", error);
    }
  };

  const handleDelete = async (itemId: string) => {
    try {
      await pantryAPI.delete(itemId);
      loadPantry(); // Reload
    } catch (error: any) {
      console.error("Error deleting item:", error);
    }
  };

  const activeItems = pantryItems.filter((item) => !item.consumed);
  const categories = ["produce", "dairy", "meat", "pantry", "frozen"];

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#D0D0D0", dark: "#1D3D47" }}
      headerImage={
        <Ionicons size={310} name="basket-outline" style={styles.headerImage} />
      }
    >
      <ThemedView style={styles.container}>
        {/* Header Section */}
        <View style={styles.titleContainer}>
          <ThemedText type="title">Virtual Pantry</ThemedText>
          <ThemedText style={styles.subtitle}>
            {activeItems.length} item{activeItems.length !== 1 ? "s" : ""} in stock
          </ThemedText>
        </View>

        {/* Category Filters */}
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false} 
          style={styles.filterContainer}
        >
          <TouchableOpacity
            style={[styles.filterButton, !filter && styles.filterButtonActive]}
            onPress={() => setFilter(null)}
          >
            <ThemedText style={[styles.filterText, !filter && styles.filterTextActive]}>
              All
            </ThemedText>
          </TouchableOpacity>
          {categories.map((cat) => (
            <TouchableOpacity
              key={cat}
              style={[styles.filterButton, filter === cat && styles.filterButtonActive]}
              onPress={() => setFilter(cat)}
            >
              <ThemedText style={[styles.filterText, filter === cat && styles.filterTextActive]}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </ThemedText>
            </TouchableOpacity>
          ))}
        </ScrollView>

        {/* Content */}
        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#22C55E" />
            <ThemedText style={styles.loadingText}>Loading pantry...</ThemedText>
          </View>
        ) : activeItems.length === 0 ? (
          <View style={styles.emptyStateContainer}>
            <Ionicons name="basket" size={80} color="#333" style={styles.emptyIcon} />
            <ThemedText type="subtitle" style={styles.emptyTitle}>
              Your pantry is empty
            </ThemedText>
            <ThemedText style={styles.emptySubtitle}>
              Scan receipts to add items
            </ThemedText>
          </View>
        ) : (
          <View style={styles.itemsList}>
            {activeItems.map((item) => (
              <IngredientCard
                key={item.item_id}
                item={item}
                onConsume={handleConsume}
                onDelete={handleDelete}
              />
            ))}
          </View>
        )}
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 16,
    minHeight: 500,
  },
  headerImage: {
    color: "#666",
    bottom: -90,
    left: -35,
    position: "absolute",
    opacity: 0.15,
  },
  titleContainer: {
    marginTop: 10,
    marginBottom: 16,
  },
  subtitle: {
    color: "#A1A1A1",
    fontSize: 16,
    marginTop: 4,
  },
  filterContainer: {
    marginBottom: 20,
  },
  filterButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    marginRight: 8,
    borderRadius: 20,
    backgroundColor: "#2A2A2A",
    borderWidth: 1,
    borderColor: "#3A3A3A",
  },
  filterButtonActive: {
    backgroundColor: "#22C55E",
    borderColor: "#22C55E",
  },
  filterText: {
    color: "#A1A1A1",
    fontSize: 14,
    fontWeight: "600",
  },
  filterTextActive: {
    color: "#fff",
  },
  loadingContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 60,
    gap: 16,
  },
  loadingText: {
    color: "#A1A1A1",
    fontSize: 16,
  },
  itemsList: {
    paddingBottom: 20,
  },
  emptyStateContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 60,
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
