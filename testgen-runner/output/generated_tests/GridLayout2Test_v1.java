package gridlayout2;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.awt.Container;
import java.awt.Dimension;

class GridLayout2Test_v1 {
 private final GridLayout2 gridLayout = new GridLayout2();
 
 @Test
 void testGridLayout2DefaultConstructor() {
 assertEquals(1, gridLayout.getRows());
 assertEquals(0, gridLayout.getColumns());
 assertEquals(0, gridLayout.getHgap());
 assertEquals(0, gridLayout.getVgap());
 }
 
 @Test
 void testGridLayout2TwoArgsConstructor() {
 GridLayout2 gl = new GridLayout2(3, 4);
 assertEquals(3, gl.getRows());
 assertEquals(4, gl.getColumns());
 assertEquals(0, gl.getHgap());
 assertEquals(0, gl.getVgap());
 }
 
 @Test
 void testGridLayout2FourArgsConstructor() {
 GridLayout2 gl = new GridLayout2(3, 4, 5, 6);
 assertEquals(3, gl.getRows());
 assertEquals(4, gl.getColumns());
 assertEquals(5, gl.getHgap());
 assertEquals(6, gl.getVgap());
 }
 
 @Test
 void testPreferredLayoutSize() {
 Container parent = null; // Assume a valid container is passed here
 Dimension expectedDimension = new Dimension(100, 100); // Set the expec[5D[K
expected dimension based on your application
 assertEquals(expectedDimension, gridLayout.preferredLayoutSize(parent))[39D[K
gridLayout.preferredLayoutSize(parent));
 }
 
 @Test
 void testMinimumLayoutSize() {
 Container parent = null; // Assume a valid container is passed here
 Dimension expectedDimension = new Dimension(100, 100); // Set the expec[5D[K
expected dimension based on your application
 assertEquals(expectedDimension, gridLayout.minimumLayoutSize(parent));
 }
}