import { useState } from "react";
import { StyleSheet, TouchableOpacity, Image, View, Alert, ActivityIndicator } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import * as ImagePicker from "expo-image-picker";

import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import ParallaxScrollView from "@/components/parallax-scroll-view";
import { receiptAPI } from "@/services/api";

export default function ScannerScreen() {
  const [image, setImage] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [receiptData, setReceiptData] = useState<any>(null);

  // Convert image to base64
  const convertToBase64 = async (uri: string): Promise<string> => {
    try {
      // For web/development, fetch the image and convert to base64
      const response = await fetch(uri);
      const blob = await response.blob();
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result as string);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    } catch (error) {
      console.error("Error converting to base64:", error);
      throw error;
    }
  };

  // Process receipt with backend
  const processReceipt = async (imageUri: string) => {
    try {
      setIsProcessing(true);
      const base64Image = await convertToBase64(imageUri);
      
      const response = await receiptAPI.upload(base64Image);
      setReceiptData(response);
      
      Alert.alert(
        "✅ Receipt Processed!",
        `Found ${response.items?.length || 0} items from ${response.store_name || 'store'}`,
        [
          {
            text: "OK",
            onPress: () => {
              // Reset for next scan
              setImage(null);
              setReceiptData(null);
            },
          },
        ]
      );
    } catch (error: any) {
      Alert.alert("Error", error.message || "Failed to process receipt");
    } finally {
      setIsProcessing(false);
    }
  };

  // Function to pick from gallery
  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImage(uri);
      await processReceipt(uri);
    }
  };

  // Function to take a photo
  const takePhoto = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();

    if (permissionResult.granted === false) {
      Alert.alert("Permission to access camera is required!");
      return;
    }

    let result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImage(uri);
      await processReceipt(uri);
    }
  };

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: "#A1CEDC", dark: "#000000" }}
      headerImage={
        <Ionicons size={310} name="scan-outline" style={styles.headerImage} />
      }
    >
      <ThemedView style={styles.container}>
        {/* Header Section */}
        <View style={styles.titleContainer}>
          <ThemedText type="title">Receipt Scanner</ThemedText>
          <ThemedText style={styles.subtitle}>
            Capture or select a receipt to analyze
          </ThemedText>
        </View>

        {/* Image Placeholder / Preview Area */}
        <View style={styles.imageContainer}>
          {image ? (
            <>
              <Image source={{ uri: image }} style={styles.image} />
              {isProcessing && (
                <View style={styles.processingOverlay}>
                  <ActivityIndicator size="large" color="#4ADE80" />
                  <ThemedText style={styles.processingText}>
                    Processing Receipt...
                  </ThemedText>
                </View>
              )}
            </>
          ) : (
            <View style={styles.placeholder}>
              <Ionicons name="receipt-outline" size={64} color="#555" />
              <ThemedText style={styles.placeholderText}>
                No receipt selected
              </ThemedText>
            </View>
          )}
        </View>

        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, { backgroundColor: "#4ADE80" }]} // Green
            onPress={takePhoto}
            disabled={isProcessing}
          >
            <Ionicons
              name="camera"
              size={24}
              color="#fff"
              style={styles.btnIcon}
            />
            <ThemedText style={styles.btnText}>Take Photo</ThemedText>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, { backgroundColor: "#3B82F6" }]} // Blue
            onPress={pickImage}
            disabled={isProcessing}
          >
            <Ionicons
              name="images"
              size={24}
              color="#fff"
              style={styles.btnIcon}
            />
            <ThemedText style={styles.btnText}>Choose from Gallery</ThemedText>
          </TouchableOpacity>
        </View>

        {/* Tips Section */}
        <View style={styles.tipsContainer}>
          <View style={styles.tipsHeader}>
            <Ionicons name="bulb-outline" size={20} color="#FFD700" />
            <ThemedText type="defaultSemiBold" style={styles.tipsTitle}>
              Tips for Best Results:
            </ThemedText>
          </View>
          <ThemedText style={styles.tipItem}>• Ensure good lighting</ThemedText>
          <ThemedText style={styles.tipItem}>
            • Capture entire receipt
          </ThemedText>
          <ThemedText style={styles.tipItem}>
            • Avoid shadows and glare
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
    gap: 24,
  },
  headerImage: {
    color: "#333", // Subtle dark grey for the parallax icon
    bottom: -90,
    left: -35,
    position: "absolute",
    opacity: 0.2,
  },
  titleContainer: {
    marginTop: 10,
    alignItems: "flex-start",
  },
  subtitle: {
    color: "#A1A1A1",
    fontSize: 16,
    marginTop: 4,
  },
  // Image Placeholder Styling
  imageContainer: {
    width: "100%",
    height: 300,
    borderRadius: 16,
    overflow: "hidden",
    marginTop: 10,
  },
  placeholder: {
    flex: 1,
    backgroundColor: "#1A1A1A", // Dark grey background
    borderWidth: 2,
    borderColor: "#333",
    borderStyle: "dashed",
    borderRadius: 16,
    justifyContent: "center",
    alignItems: "center",
  },
  placeholderText: {
    color: "#555",
    marginTop: 12,
    fontSize: 16,
  },
  image: {
    width: "100%",
    height: "100%",
    resizeMode: "contain",
  },
  // Button Styling
  buttonContainer: {
    gap: 16,
  },
  button: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 16,
    borderRadius: 12,
    width: "100%",
  },
  btnIcon: {
    marginRight: 8,
  },
  btnText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "bold",
  },
  // Tips Section Styling
  tipsContainer: {
    backgroundColor: "#1A1A1A",
    borderRadius: 12,
    padding: 16,
    marginTop: 8,
  },
  tipsHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
    gap: 8,
  },
  tipsTitle: {
    fontSize: 16,
    color: "#fff",
  },
  tipItem: {
    color: "#A1A1A1",
    fontSize: 14,
    marginLeft: 4,
    marginTop: 4,
  },
  processingOverlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: "rgba(0, 0, 0, 0.7)",
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 16,
  },
  processingText: {
    color: "#fff",
    marginTop: 16,
    fontSize: 16,
    fontWeight: "600",
  },
});
