package extboolarray;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class ExtBoolArrayTest_v1 {
 @Test
 void testSetTrue() {
 ExtBoolArray boolArray = new ExtBoolArray(5);
 boolArray.setTrue(1, 3); // setting values from index 1 to 3 as true
 
 assertFalse(boolArray.isFalse(0, 0)); // should return false for isFalse method on indices 0-0 as this value is set to true
 assertFalse(boolArray.isFalse(2, 4)); // should return false for isFalse method on indices 2-4 since none of these are initially set to false
 }
 
 @Test
 void testIsFalse() {
 boolArray.setTrue(1, 3); // setting values from index 1 to 3 as true
 
 assertFalse(boolArray.isFalse(1, 3)); // should return false for isFalse method on indices 1-3
 }
 
 @Test
 void testLeft() {
 boolArray.setTrue(0, 2); // setting values from index 0 to 2 as true
 
 assertEquals(2, boolArray.left()); // should return 3 for left method because all the remaining indices are false
 }
}