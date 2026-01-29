import { View, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";

interface ComparisonCardProps {
  comparison: {
    delivery_item: {
      name: string;
      restaurant: string;
      price: number;
      calories?: number;
    };
    home_cooking_alternative: {
      recipe_name: string;
      estimated_cost: number;
      ingredients: string[];
      calories?: number;
      prep_time?: number;
    };
    savings: number;
    calorie_difference?: number;
  };
  recommendation?: string;
}

export default function ComparisonCard({ comparison, recommendation }: ComparisonCardProps) {
  const { delivery_item, home_cooking_alternative, savings, calorie_difference } = comparison;

  return (
    <ThemedView style={styles.container}>
      {/* Delivery Option */}
      <View style={styles.optionCard}>
        <View style={styles.optionHeader}>
          <Ionicons name="fast-food" size={24} color="#F59E0B" />
          <ThemedText style={styles.optionTitle}>Delivery</ThemedText>
        </View>
        <ThemedText style={styles.itemName}>{delivery_item.name}</ThemedText>
        <ThemedText style={styles.restaurant}>{delivery_item.restaurant}</ThemedText>
        <View style={styles.statsRow}>
          <View style={styles.stat}>
            <ThemedText style={styles.statLabel}>Price</ThemedText>
            <ThemedText style={styles.statValue}>${delivery_item.price.toFixed(2)}</ThemedText>
          </View>
          {delivery_item.calories && (
            <View style={styles.stat}>
              <ThemedText style={styles.statLabel}>Calories</ThemedText>
              <ThemedText style={styles.statValue}>{Math.round(delivery_item.calories)}</ThemedText>
            </View>
          )}
        </View>
      </View>

      {/* VS Divider */}
      <View style={styles.divider}>
        <ThemedText style={styles.vsText}>VS</ThemedText>
      </View>

      {/* Home Cooking Option */}
      <View style={styles.optionCard}>
        <View style={styles.optionHeader}>
          <Ionicons name="home" size={24} color="#22C55E" />
          <ThemedText style={styles.optionTitle}>Home Cooked</ThemedText>
        </View>
        <ThemedText style={styles.itemName}>{home_cooking_alternative.recipe_name}</ThemedText>
        {home_cooking_alternative.prep_time && (
          <ThemedText style={styles.restaurant}>
            ~{home_cooking_alternative.prep_time} minutes
          </ThemedText>
        )}
        <View style={styles.statsRow}>
          <View style={styles.stat}>
            <ThemedText style={styles.statLabel}>Est. Cost</ThemedText>
            <ThemedText style={styles.statValue}>
              ${home_cooking_alternative.estimated_cost.toFixed(2)}
            </ThemedText>
          </View>
          {home_cooking_alternative.calories && (
            <View style={styles.stat}>
              <ThemedText style={styles.statLabel}>Calories</ThemedText>
              <ThemedText style={styles.statValue}>
                {Math.round(home_cooking_alternative.calories)}
              </ThemedText>
            </View>
          )}
        </View>
      </View>

      {/* Savings Summary */}
      <View style={styles.summaryCard}>
        <View style={styles.summaryRow}>
          <ThemedText style={styles.summaryLabel}>💰 Cost Savings</ThemedText>
          <ThemedText style={[styles.summaryValue, savings > 0 && styles.positiveValue]}>
            ${Math.abs(savings).toFixed(2)}
          </ThemedText>
        </View>
        {calorie_difference !== null && calorie_difference !== undefined && (
          <View style={styles.summaryRow}>
            <ThemedText style={styles.summaryLabel}>🥗 Calorie Difference</ThemedText>
            <ThemedText style={[styles.summaryValue, calorie_difference > 0 && styles.positiveValue]}>
              {Math.abs(calorie_difference)} cal
            </ThemedText>
          </View>
        )}
      </View>

      {/* Recommendation */}
      {recommendation && (
        <View style={styles.recommendationCard}>
          <ThemedText style={styles.recommendationText}>{recommendation}</ThemedText>
        </View>
      )}

      {/* Ingredients List */}
      {home_cooking_alternative.ingredients && home_cooking_alternative.ingredients.length > 0 && (
        <View style={styles.ingredientsCard}>
          <ThemedText style={styles.ingredientsTitle}>📝 Ingredients Needed:</ThemedText>
          {home_cooking_alternative.ingredients.slice(0, 5).map((ingredient, index) => (
            <ThemedText key={index} style={styles.ingredientItem}>
              • {ingredient}
            </ThemedText>
          ))}
          {home_cooking_alternative.ingredients.length > 5 && (
            <ThemedText style={styles.moreText}>
              +{home_cooking_alternative.ingredients.length - 5} more...
            </ThemedText>
          )}
        </View>
      )}
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: 16,
  },
  optionCard: {
    backgroundColor: "#1A1A1A",
    borderRadius: 12,
    padding: 16,
    borderWidth: 2,
    borderColor: "#2A2A2A",
  },
  optionHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 12,
  },
  optionTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#A1A1A1",
  },
  itemName: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 4,
  },
  restaurant: {
    fontSize: 14,
    color: "#888",
    marginBottom: 12,
  },
  statsRow: {
    flexDirection: "row",
    gap: 16,
  },
  stat: {
    flex: 1,
  },
  statLabel: {
    fontSize: 12,
    color: "#888",
    marginBottom: 4,
  },
  statValue: {
    fontSize: 18,
    fontWeight: "600",
  },
  divider: {
    alignItems: "center",
    paddingVertical: 8,
  },
  vsText: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#555",
    backgroundColor: "#2A2A2A",
    paddingHorizontal: 16,
    paddingVertical: 4,
    borderRadius: 12,
  },
  summaryCard: {
    backgroundColor: "#1E3A2F",
    borderRadius: 12,
    padding: 16,
    borderWidth: 2,
    borderColor: "#22C55E",
  },
  summaryRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  summaryLabel: {
    fontSize: 16,
    fontWeight: "600",
  },
  summaryValue: {
    fontSize: 18,
    fontWeight: "bold",
  },
  positiveValue: {
    color: "#22C55E",
  },
  recommendationCard: {
    backgroundColor: "#2A2A2A",
    borderRadius: 12,
    padding: 16,
  },
  recommendationText: {
    fontSize: 15,
    lineHeight: 22,
    color: "#E5E5E5",
  },
  ingredientsCard: {
    backgroundColor: "#1A1A1A",
    borderRadius: 12,
    padding: 16,
  },
  ingredientsTitle: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 12,
  },
  ingredientItem: {
    fontSize: 14,
    color: "#A1A1A1",
    marginBottom: 6,
  },
  moreText: {
    fontSize: 14,
    color: "#888",
    fontStyle: "italic",
    marginTop: 4,
  },
});
