import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { StyleSheet, View, Dimensions } from "react-native";
import { LineChart } from "react-native-gifted-charts";

type ChartCardProps = {
  title: string;
  color: string;
  data: { value: number; label?: string }[];
};

export default function ChartCard({ title, color, data }: ChartCardProps) {
  const screenWidth = Dimensions.get("window").width;

  return (
    <ThemedView style={styles.container}>
      <ThemedText type="defaultSemiBold" style={styles.title}>
        {title}
      </ThemedText>

      <View style={styles.chartWrapper}>
        <LineChart
          data={data}
          areaChart
          curved
          // Dimensions
          height={120}
          width={screenWidth - 80} // Adjust for padding
          // Styling - Lines & Area
          color={color}
          thickness={3}
          startFillColor={color}
          endFillColor={color}
          startOpacity={0.4}
          endOpacity={0.1}
          // Styling - Grid & Axis
          hideYAxisText={false}
          yAxisTextStyle={{ color: "#666", fontSize: 10 }}
          yAxisColor="transparent"
          xAxisColor="transparent"
          rulesType="dashed"
          rulesColor="#333"
          // Styling - Data Points
          hideDataPoints={false}
          dataPointsColor={color}
          dataPointsRadius={3}
          // Pointer / Interaction
          pointerConfig={{
            pointerStripHeight: 120,
            pointerStripColor: "#333",
            pointerStripWidth: 2,
            pointerColor: color,
            radius: 4,
            pointerLabelWidth: 100,
            pointerLabelHeight: 120,
            activatePointersOnLongPress: true,
            autoAdjustPointerLabelPosition: false,
            pointerLabelComponent: (items: any) => {
              return (
                <View style={styles.pointerLabel}>
                  <ThemedText style={styles.pointerText}>
                    {items[0].value}
                  </ThemedText>
                </View>
              );
            },
          }}
        />
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 20,
  },
  title: {
    marginBottom: 10,
    fontSize: 16,
    color: "#fff", // Adjust based on your theme
  },
  chartWrapper: {
    backgroundColor: "#111827", // Dark card background
    borderRadius: 16,
    paddingVertical: 16,
    paddingHorizontal: 0, // Padding handled by chart props
    overflow: "hidden",
  },
  pointerLabel: {
    height: 30,
    width: 40,
    backgroundColor: "black",
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 4,
  },
  pointerText: {
    color: "white",
    fontSize: 12,
    fontWeight: "bold",
  },
});
