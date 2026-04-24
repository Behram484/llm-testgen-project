package org.jcvi.jillion.core.util;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import java.math.BigInteger;
import java.util.*;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class MathUtilTest_v1 {
 
 @Test
 public void testMinOfCollection() {
 List<Integer> numbers = Arrays.asList(2, 1, 3);
 assertEquals((long)MathUtil.minOf(numbers), 1L);
 }
 
 @Test
 public void testMaxOfCollection() {
 List<Double> numbers = Arrays.asList(0.5, 1.2, -1.8);
 assertEquals((double)MathUtil.maxOf(numbers), 1.2);
 }
 
 @Test
 public void testAverageOfCollection() {
 List<Integer> numbers = Arrays.asList(-5, -4, -3, -2, -1, 0, 1, 2, 3, 4,[2D[K
4, 5);
 assertEquals((double)MathUtil.averageOf(numbers), 0.0);
 }
 
 @Test
 public void testSumOfCollection() {
 List<Integer> numbers = Arrays.asList(-1, -2, -3, -4, -5);
 assertEquals((long)MathUtil.sumOf(numbers), -15L);
 }
 
 @Test
 public void testMinOfVarargs() {
 Integer[] numbers = new Integer[]{2, 1, 3};
 Assertions.assertEquals((long)MathUtil.minOf(Arrays.asList(numbers)), 1L[2D[K
1L);
 }
 
 @Test
 public void testMaxOfVarargs() {
 Double[] numbers = new Double[]{0.5, 1.2, -1.8};
 Assertions.assertEquals((double)MathUtil.maxOf(Arrays.asList(numbers)), [K
1.2);
 }
 
 @Test
 public void testAverageOfVarargs() {
 Integer[] numbers = new Integer[]{-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5};[3D[K
5};
 Assertions.assertEquals((double)MathUtil.averageOf(Arrays.asList(numb[69D[K
Assertions.assertEquals((double)MathUtil.averageOf(Arrays.asList(numbers)),Assertions.assertEquals((double)MathUtil.averageOf(Arrays.asList(numbrs)), 0.0);
 }
 
 @Test
 public void testSumOfVarargs() {
 Integer[] numbers = new Integer[]{1, 2, 3, 4, 5};
 Assertions.assertEquals((long)MathUtil.sumOf(Arrays.asList(numbers)), 15[2D[K
15L);
 }
}