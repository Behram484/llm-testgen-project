package src.feudalismGUI;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.awt.Container;
import java.awt.Dimension;

public class GridLayout2Test_v1 {
 private GridLayout2 layout;
 private Container parent;

 @BeforeEach
 public void setUp() {
 layout = new GridLayout2(3, 3);
 parent = new Container() {
 @Override
 public Dimension getPreferredSize() {
 return new Dimension(800, 600);
 }
 };
 }

 @Test
 public void testDefaultConstructor() {
 GridLayout2 defaultLayout = new GridLayout2();
 assertEquals(1, defaultLayout.getRows());
 assertEquals(0, defaultLayout.getColumns());
 assertEquals(0, defaultLayout.getHgap());
 assertEquals(0, defaultLayout.getVgap());
 }

 @Test
 public void testTwoArgumentConstructor() {
 GridLayout2 twoArgLayout = new GridLayout2(5, 7);
 assertEquals(5, twoArgLayout.getRows());
 assertEquals(7, twoArgLayout.getColumns());
 assertEquals(0, twoArgLayout.getHgap());
 assertEquals(0, twoArgLayout.getVgap());
 }

 @Test
 public void testFourArgumentConstructor() {
 GridLayout2 fourArgLayout = new GridLayout2(5, 7, 10, 15);
 assertEquals(5, fourArgLayout.getRows());
 assertEquals(7, fourArgLayout.getColumns());
 assertEquals(10, fourArgLayout.getHgap());
 assertEquals(15, fourArgLayout.getVgap());
 }

 @Test
 public void testPreferredLayoutSize() {
 Dimension preferred = layout.preferredLayoutSize(parent);
 assertEquals(0, preferred.width);
 assertEquals(0, preferred.height);
 }

 @Test
 public void testMinimumLayoutSize() {
 Dimension min = layout.minimumLayoutSize(parent);
 assertEquals(0, min.width);
 assertEquals(0, min.height);
 }
}