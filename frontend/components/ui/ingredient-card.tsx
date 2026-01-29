import { View, StyleSheet, TouchableOpacity, Alert } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";

interface IngredientCardProps {
  item: {
    item_id: string;
    name: string;
    category: string;
    quantity: number;
    unit: string;
    expiration_date: string;
    urgency?: string;
    urgency_color?: string;
    days_until_expiration?: number;
    calories?: number;
    protein?: number;
  };
  onConsume?: (itemId: string) => void;
  onDelete?: (itemId: string) => void;
}

const categoryIcons: { [key: string]: any } = {
  produce: "leaf",
  dairy: "water",
  meat: "restaurant",
  pantry: "cube",
  frozen: "snow",
  beverages: "wine",
  snacks: "fast-food",
  other: "basket",
};

export default function IngredientCard({ item, onConsume, onDelete }: IngredientCardProps) {
  const handleConsume = () => {
    Alert.alert(
      "Mark as Consumed",
      `Did you consume ${item.name}?`,
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Yes",
          onPress: () => onConsume?.(item.item_id),
        },
      ]
    );
  };

  const handleDelete = () => {
    Alert.alert(
      "Delete Item",
      `Remove ${item.name} from pantry?`,
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Delete",
          style: "destructive",
          onPress: () => onDelete?.(item.item_id),
        },
      ]
    );
  };

  const getUrgencyLabel = () => {
    if (item.urgency === "expired") return "Expired";
    if (item.urgency === "expires_today") return "Expires Today";
    if (item.urgency === "urgent") return `${item.days_until_expiration}d left`;
    if (item.urgency === "warning") return `${item.days_until_expiration}d left`;
    return `${item.days_until_expiration}d left`;
  };

  return (
    <ThemedView style={[styles.card, { borderLeftColor: item.urgency_color || "#22C55E", borderLeftWidth: 4 }]}>
      <View style={styles.mainContent}>
        <View style={styles.iconContainer}>
          <Ionicons
            name={categoryIcons[item.category] || "basket"}
            size={32}
            color={item.urgency_color || "#22C55E"}
          />
        </View>

        <View style={styles.infoContainer}>
          <ThemedText style={styles.itemName}>{item.name}</ThemedText>
          <View style={styles.detailsRow}>
            <ThemedText style={styles.quantity}>
              {item.quantity} {item.unit}
            </ThemedText>
            <ThemedText style={styles.separator}>•</ThemedText>
            <ThemedText style={styles.category}>{item.category}</ThemedText>
          </View>
          {(item.calories || item.protein) && (
            <View style={styles.nutritionRow}>
              {item.calories && (
                <ThemedText style={styles.nutritionText}>
                  {Math.round(item.calories)} cal
                </ThemedText>
              )}
              {item.protein && (
                <ThemedText style={styles.nutritionText}>
                  {item.protein.toFixed(1)}g protein
                </ThemedText>
              )}
            </View>
          )}
        </View>

        <View style={styles.expirationContainer}>
          <View style={[styles.expirationBadge, { backgroundColor: item.urgency_color || "#22C55E" }]}>
            <ThemedText style={styles.expirationText}>{getUrgencyLabel()}</ThemedText>
          </View>
        </View>
      </View>

      <View style={styles.actionsContainer}>
        <TouchableOpacity style={[styles.actionButton, styles.consumeButton]} onPress={handleConsume}>
          <Ionicons name="checkmark-circle" size={20} color="#22C55E" />
          <ThemedText style={styles.consumeText}>Consumed</ThemedText>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.actionButton, styles.deleteButton]} onPress={handleDelete}>
          <Ionicons name="trash" size={20} color="#EF4444" />
          <ThemedText style={styles.deleteText}>Remove</ThemedText>
        </TouchableOpacity>
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    backgroundColor: "#1A1A1A",
  },
  mainContent: {
    flexDirection: "row",
    alignItems: "flex-start",
    marginBottom: 12,
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: "#2A2A2A",
    justifyContent: "center",
    alignItems: "center",
    marginRight: 12,
  },
  infoContainer: {
    flex: 1,
  },
  itemName: {
    fontSize: 18,
    fontWeight: "600",
    marginBottom: 4,
  },
  detailsRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 4,
  },
  quantity: {
    fontSize: 14,
    color: "#A1A1A1",
  },
  separator: {
    fontSize: 14,
    color: "#555",
    marginHorizontal: 6,
  },
  category: {
    fontSize: 14,
    color: "#A1A1A1",
    textTransform: "capitalize",
  },
  nutritionRow: {
    flexDirection: "row",
    gap: 12,
    marginTop: 4,
  },
  nutritionText: {
    fontSize: 12,
    color: "#888",
  },
  expirationContainer: {
    marginLeft: 8,
  },
  expirationBadge: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  expirationText: {
    color: "#fff",
    fontSize: 12,
    fontWeight: "600",
  },
  actionsContainer: {
    flexDirection: "row",
    gap: 8,
    borderTopWidth: 1,
    borderTopColor: "#2A2A2A",
    paddingTop: 12,
  },
  actionButton: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 10,
    borderRadius: 8,
    gap: 6,
  },
  consumeButton: {
    backgroundColor: "rgba(34, 197, 94, 0.1)",
    borderWidth: 1,
    borderColor: "#22C55E",
  },
  deleteButton: {
    backgroundColor: "rgba(239, 68, 68, 0.1)",
    borderWidth: 1,
    borderColor: "#EF4444",
  },
  consumeText: {
    color: "#22C55E",
    fontSize: 14,
    fontWeight: "600",
  },
  deleteText: {
    color: "#EF4444",
    fontSize: 14,
    fontWeight: "600",
  },
});
