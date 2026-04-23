package extboolarray;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test; // corrected th[2D[K
this line to be "org.junit.jupiter.api.Test"

public class ExtBoolArrayTest_v1 {
 private ExtBoolArray array;
 
 @BeforeEach
 public void setUp() {
 array = new ExtBoolArray(5); // Initialize array of size 5 for tes[3D[K
testing
 }

 @Test
 public void testIsFalse() {
 array.setTrue(0, 2);
 assertTrue(array.isFalse(3, 4)); // Check if the range [3,4] is al[2D[K
all false
 assertTrue(array.isFalse(1, 1)); // Check if index 1 is false
 }
 
 @Test
 public void testSetTrue() {
 array.setTrue(0, 2);
 assertTrue(array.isFalse(3, 4)); // Check if the range [3,4] is al[2D[K
all false
 assertEquals(3, array.left()); // Verify remaining false elements
 }
 
 @Test
 public void testLeft() {
 array.setTrue(0, 2);
 assertEquals(3, array.left());
 
 array.setTrue(1, 1);
 assertEquals(3, array.left());
 }
}