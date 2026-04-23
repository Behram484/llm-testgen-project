package mathutil;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.math.BigInteger;
import java.util.Arrays;

public class MathUtilTest_v1 {
 private final MathUtil mathUtil = new MathUtil(); // Create instance of[2D[K
of MathUtil to call its methods
 
 @Test
 void testMinOfCollection() {
 assertEquals(5, mathUtil.minOf(Arrays.asList(9, 7, 4, 2, 3, 6, 8, 0, [K
5)));
 }

 @Test
 void testMinOfArray() {
 assertThrows(IllegalArgumentException.class, () -> mathUtil.minOf(-1L[18D[K
mathUtil.minOf(-1L, -2L, 3L));
 }

 @Test
 void testMaxOfCollection() {
 assertEquals(9L, mathUtil.maxOf(Arrays.asLis[7D[K
>.asList(9L, 7L, 4L, 2L, 3L, 6L, 8L, 0L, 5L)));
 }

 @Test
 void testMaxOfArray() {
 assertThrows(IllegalArgumentException.class, () -> mathUtil.maxOf(-1L[18D[K
mathUtil.maxOf(-1L, -2L, 3L));
 }

 @Test
 void testAverageOfCollection() {
 assertEquals(4.0, mathUtil.averageOf(Arrays.asList(9L, 7L, 4L, 2L, 3L[2D[K
3L, 6L, 8L, 0L, 5L)));
 }

 @Test
 void testAverageOfArray() {
 assertThrows(IllegalArgumentException.class, () -> mathUtil.averageOf[18D[K
mathUtil.averageOf(-1L, -2L, 3L));
 }

 @Test
 void testSumOfByteArray() {
 assertEquals(BigInteger.valueOf(4), mathUtil.sumOf(new byte[]{1, 1, 1[1D[K
1, 1, 1}));
 }

 @Test
 void testSumOfIntArray() {
 assertEquals(BigInteger.valueOf(6), mathUtil.sumOf(new int[]{1, 2, 3}[2D[K
3}));
 }

 @Test
 void testSumOfLongArray() {
 assertEquals(BigInteger.valueOf(8L), mathUtil.sumOf(new long[]{1L, 1L[2D[K
1L, 1L, 1L, 1L, 2L, 3L, 2L}));
 }

 @Test
 void testSumOfShortArray() {
 assertEquals(BigInteger.valueOf(6), mathUtil.sumOf(new short[]{1, 2, [K
3}));
 }

 @Test
 void testSumOfCollection() {
 assertEquals(BigInteger.valueOf(15L), mathUtil.sumOf(Arrays.asList(9L[31D[K
mathUtil.sumOf(Arrays.asList(9L, 7L, 4L, 2L)));
 }
}