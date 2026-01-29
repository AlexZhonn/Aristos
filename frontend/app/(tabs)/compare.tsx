import { useState } from "react";
import {
  StyleSheet,
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import * as ImagePicker from "expo-image-picker";

import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import ParallaxScrollView from "@/components/parallax-scroll-view";
import ComparisonCard from "@/components/ui/comparison-card";
import { comparisonAPI } from "@/services/api";

export default function CompareScreen() {
  const [itemName, setItemName] = useState("");
  const [restaurant, setRestaurant] = useState("");
  const [price, setPrice] = useState("");
  const [image, setImage] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  const analyzeDelivery = async () => {
    if (!itemName || !restaurant || !price) {
      Alert.alert("Missing Information", "Please fill in all required fields");
      return;
    }

    try {
      setIsAnalyzing(true);
      
      let imageBase64 = undefined;
      if (image) {
        // Convert image to base64
        const response = await fetch(image);
        const blob = await response.blob();
        imageBase64 = await new Promise<string>((resolve, reject) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result as string);
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });
      }

      const deliveryItem = {
        name: itemName,
        restaurant: restaurant,
        price: parseFloat(price),
      };

      const response = await comparisonAPI.analyze(deliveryItem, imageBase64);
      setResult(response);
    } catch (error: any) {
      Alert.alert("Error", error.message || "Failed to analyze delivery item");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetForm = () => {
    setItemName("");
    setRestaurant("");
    setPrice("");
    setImage(null);
    setResult(null);
  };

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#A1CEDC", dark: "#1D3D47" }}
      headerImage={
        <Ionicons size={310} name="analytics-outline" style={styles.headerImage} />
      }
    >
      <ThemedView style={styles.container}>
        <View style={styles.titleContainer}>
          <ThemedText type="title">Delivery vs Home</ThemedText>
          <ThemedText style={styles.subtitle}>
            Compare costs and make smarter choices
          </ThemedText>
        </View>

        {!result ? (
          <>
            {/* Input Form */}
            <View style={styles.form}>
              <View style={styles.inputGroup}>
                <ThemedText style={styles.label}>Dish Name *</ThemedText>
                <TextInput
                  style={styles.input}
                  placeholder="e.g., Pad Thai, Burger, Pizza"
                  placeholderTextColor="#666"
                  value={itemName}
                  onChangeText={setItemName}
                />
              </View>

              <View style={styles.inputGroup}>
                <ThemedText style={styles.label}>Restaurant *</ThemedText>
                <TextInput
                  style={styles.input}
                  placeholder="e.g., Thai Express, McDonald's"
                  placeholderTextColor="#666"
                  value={restaurant}
                  onChangeText={setRestaurant}
                />
              </View>

              <View style={styles.inputGroup}>
                <ThemedText style={styles.label}>Price ($) *</ThemedText>
                <TextInput
                  style={styles.input}
                  placeholder="e.g., 15.99"
                  placeholderTextColor="#666"
                  keyboardType="decimal-pad"
                  value={price}
                  onChangeText={setPrice}
                />
              </View>

              {/* Optional Image */}
              <View style={styles.inputGroup}>
                <ThemedText style={styles.label}>Photo (Optional)</ThemedText>
                {image ? (
                  <View style={styles.imagePreview}>
                    <TouchableOpacity style={styles.removeImage} onPress={() => setImage(null)}>
                      <Ionicons name="close-circle" size={24} color="#EF4444" />
                    </TouchableOpacity>
                    <View style={styles.imageContainer}>
                      {/* eslint-disable-next-line @typescript-eslint/no-var-requires */}
                      <img src={image} style={{ width: "100%", height: "100%", objectFit: "cover" }} alt="Food" />
                    </View>
                  </View>
                ) : (
                  <TouchableOpacity style={styles.imagePicker} onPress={pickImage}>
                    <Ionicons name="camera" size={32} color="#888" />
                    <ThemedText style={styles.imagePickerText}>Add Photo</ThemedText>
                  </TouchableOpacity>
                )}
              </View>

              {/* Analyze Button */}
              <TouchableOpacity
                style={[styles.analyzeButton, isAnalyzing && styles.analyzeButtonDisabled]}
                onPress={analyzeDelivery}
                disabled={isAnalyzing}
              >
                {isAnalyzing ? (
                  <>
                    <ActivityIndicator color="#fff" />
                    <ThemedText style={styles.analyzeButtonText}>Analyzing...</ThemedText>
                  </>
                ) : (
                  <>
                    <Ionicons name="analytics" size={20} color="#fff" />
                    <ThemedText style={styles.analyzeButtonText}>Compare Options</ThemedText>
                  </>
                )}
              </TouchableOpacity>
            </View>
          </>
        ) : (
          <>
            {/* Comparison Result */}
            <ComparisonCard comparison={result.comparison} recommendation={result.recommendation} />

            {/* Action Buttons */}
            <View style={styles.actionButtons}>
              <TouchableOpacity style={styles.newComparisonButton} onPress={resetForm}>
                <Ionicons name="refresh" size={20} color="#3B82F6" />
                <ThemedText style={styles.newComparisonText}>New Comparison</ThemedText>
              </TouchableOpacity>
            </View>
          </>
        )}
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 16,
    paddingBottom: 24,
  },
  headerImage: {
    color: "#333",
    bottom: -90,
    left: -35,
    position: "absolute",
    opacity: 0.2,
  },
  titleContainer: {
    marginTop: 10,
    marginBottom: 24,
  },
  subtitle: {
    color: "#A1A1A1",
    fontSize: 16,
    marginTop: 4,
  },
  form: {
    gap: 20,
  },
  inputGroup: {
    gap: 8,
  },
  label: {
    fontSize: 14,
    fontWeight: "600",
    color: "#E5E5E5",
  },
  input: {
    backgroundColor: "#1A1A1A",
    borderWidth: 1,
    borderColor: "#2A2A2A",
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: "#E5E5E5",
  },
  imagePicker: {
    backgroundColor: "#1A1A1A",
    borderWidth: 2,
    borderColor: "#2A2A2A",
    borderStyle: "dashed",
    borderRadius: 12,
    paddingVertical: 32,
    alignItems: "center",
    gap: 8,
  },
  imagePickerText: {
    color: "#888",
    fontSize: 14,
  },
  imagePreview: {
    position: "relative",
  },
  imageContainer: {
    width: "100%",
    height: 200,
    borderRadius: 12,
    overflow: "hidden",
    backgroundColor: "#1A1A1A",
  },
  removeImage: {
    position: "absolute",
    top: 8,
    right: 8,
    zIndex: 10,
    backgroundColor: "#000",
    borderRadius: 12,
  },
  analyzeButton: {
    backgroundColor: "#22C55E",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    paddingVertical: 16,
    borderRadius: 12,
    marginTop: 8,
  },
  analyzeButtonDisabled: {
    opacity: 0.6,
  },
  analyzeButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
  actionButtons: {
    marginTop: 20,
    gap: 12,
  },
  newComparisonButton: {
    backgroundColor: "rgba(59, 130, 246, 0.1)",
    borderWidth: 2,
    borderColor: "#3B82F6",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    paddingVertical: 14,
    borderRadius: 12,
  },
  newComparisonText: {
    color: "#3B82F6",
    fontSize: 16,
    fontWeight: "600",
  },
});
