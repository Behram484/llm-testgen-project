package gridlayout2;

import static org.junit.jupiter.api.Assertions.*;
import java.awt.Container;
import java.awt.Dimension;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JPanel;
import org.junit.jupiter.api.Test;

class GridLayout2Test_v1 {
 
 @Test
 void testGridLayout2() {
 GridLayout2 layout = new GridLayout2(3, 4, 5, 6);
 
 assertEquals(3, layout.getRows());
 assertEquals(4, layout.getColumns());
 assertEquals(5, layout.getHgap());
 assertEquals(6, layout.getVgap());
 }
 
 @Test
 void testPreferredLayoutSize() {
 GridLayout2 layout = new GridLayout2();
 Container parent = new JPanel();
 
 List<Component> components = new ArrayList<>();
 for (int i = 0; i < 10; i++) {
 Component c = new ComponentMock(new Dimension(i * 5, i * 4));
 components.add(c);
 parent.add(c);
 }
 
 Dimension expectedSize = new Dimension(275, 360);
 assertEquals(expectedSize, layout.preferredLayoutSize(parent));
 }
 
 @Test
 void testMinimumLayoutSize() {
 GridLayout2 layout = new GridLayout2();
 Container parent = new JPanel();
 
 List<Component> components = new ArrayList<>();
 for (int i = 0; i < 10; i++) {
 Component c = new ComponentMock(new Dimension(i * 5, i * 4));
 components.add(c);
 parent.add(c);
 }
 
 Dimension expectedSize = new Dimension(275, 360);
 assertEquals(expectedSize, layout.minimumLayoutSize(parent));
 }
 
 @Test
 void testLayoutContainer() {
 GridLayout2 layout = new GridLayout2();
 Container parent = new JPanel();
 
 List<Component> components = new ArrayList<>();
 for (int i = 0; i < 10; i++) {
 Component c = new ComponentMock(new Dimension(i * 5, i * 4));
 components.add(c);
 parent.add(c);
 }
 
 layout.layoutContainer(parent);
 
 for (int i = 0; i < 10; i++) {
 assertEquals(components.get(i).getBounds(), parent.getComponent(i).getBounds());
 }
 }
}

class ComponentMock extends javax.swing.JLabel implements java.awt.Component {
 
 public ComponentMock(Dimension d) {
 super();
 setPreferredSize(d);
 setMinimumSize(d);
 }
}