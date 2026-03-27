package arrayutil;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public final class ArrayUtilTest_v1 {
 @Test 
 void testArrayMax() {
 Integer[] arr = {3, 2, 1};
 assertSame(ArrayUtil.arrayMax(arr), 3);
 }

 @Test
 void testArrayMin() {
 Integer[] arr = {3, 2, 1};
 assertSame(ArrayUtil.arrayMin(arr), 1);
 }

 @Test 
 void testBox() {
 int[][] data = {{1, 2}, {3, 4}};
 Integer[][] expected = {{1, 2}, {3, 4}};
 assertArrayEquals(ArrayUtil.box(data), expected);
 }
 
 @Test 
 void testRowMajorToColumnMajor() {
 int[][] rowMajor = {{1, 2}, {3, 4}};
 int[][] expected = {{1, 3}, {2, 4}};
 assertArrayEquals(ArrayUtil.rowMajorToColumnMajor(rowMajor), expected);
 }
}