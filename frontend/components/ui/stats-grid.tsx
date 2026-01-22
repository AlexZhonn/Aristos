import { ThemedText } from "../themed-text";
import { ThemedView } from "../themed-view";
import { StyleSheet } from "react-native";
type StatsGridProps = {
  backgroundColor: string | undefined;
  borderColor: string | undefined;
  title: string | undefined;
};
export default function StatsGrid({
  backgroundColor,
  borderColor,
  title,
}: StatsGridProps) {
  return (
    <ThemedView
      style={[
        styles.grid,
        borderColor ? { borderColor: borderColor } : undefined,
        backgroundColor ? { backgroundColor: backgroundColor } : undefined,
      ]}
    >
      <ThemedText style={styles.text}>{title}</ThemedText>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  grid: {
    alignItems: "center",
    borderRadius: 10,
    backgroundColor: "#00004d",
    height: 200,
    width: 150,
    opacity: 0.9,
    borderWidth: 1,
  },
  text: {
    fontSize: 19,
    fontFamily: "Gill Sans",
    color: "#ffffff",
  },
});
