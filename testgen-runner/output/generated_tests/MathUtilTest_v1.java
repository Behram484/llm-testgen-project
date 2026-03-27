package mathutil;

import org.junit.jupiter.api.*;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class MathUtilTest_v1 {
 @Test
 public void testMinOf() {
 List<Integer> numbers = Arrays.asList(3, 1, 2);
 assertEquals((long)MathUtil.minOf(numbers), (long)Collections.min(numbers));
 
 Integer[] arrayNumbers = new Integer[]{4567, -9870, 1234};
 assertEquals((long)MathUtil.minOf(arrayNumbers), (long)Collections.min(Arrays.asList(arrayNumbers)));
 }
 
 @Test
 public void testMaxOf() {
 List<Integer> numbers = Arrays.asList(-3, -1, 2);
 assertEquals((long)MathUtil.maxOf(numbers), (long)Collections.max(numbers));
 
 Integer[] arrayNumbers = new Integer[]{4567, -9870, 1234};
 assertEquals((long)MathUtil.maxOf(arrayNumbers), (long)Collections.max(Arrays.asList(arrayNumbers)));
 }
 
 @Test
 public void testAverageOf() {
 List<Integer> numbers = Arrays.asList(-3, -1, 2);
 double sum = 0;
 for (int num : numbers) {
 sum += num;
 }
 assertEquals(MathUtil.averageOf(numbers), sum / numbers.size());
 
 Integer[] arrayNumbers = new Integer[]{4567, -9870, 1234};
 sum = 0;
 for (int num : arrayNumbers) {
 sum += num;
 }
 assertEquals(MathUtil.averageOf(arrayNumbers), sum / arrayNumbers.length);
 }
 
 @Test
 public void testSumOf() {
 List<Integer> numbers = Arrays.asList(-3, -1, 2);
 BigInteger sum = new BigInteger("0");
 for (int num : numbers) {
 sum = sum.add(BigInteger.valueOf(num));
 }
 assertEquals(MathUtil.sumOf(new MathUtil(), numbers), sum); 
 
 Integer[] arrayNumbers = new Integer[]{4567, -9870, 1234};
 sum = new BigInteger("0");
 for (int num : arrayNumbers) {
 sum = sum.add(BigInteger.valueOf(num));
 }
 assertEquals(MathUtil.sumOf(new MathUtil(), arrayNumbers), sum); 
 }
 
 @Test
 public void testMedianOf() {
 List<Integer> numbers = Arrays.asList(-3, -1, 2);
 Collections.sort(numbers);
 int size = numbers.size();
 if (size % 2 == 0) {
 assertEquals((long)MathUtil.medianOf(numbers), ((long)numbers.get(size / 2 - 1) + (long)numbers.get(size / 2)) / 2);
 } else {
 assertEquals((long)MathUtil.medianOf(numbers), (long)numbers.get(size / 2));
 }
 
 Integer[] arrayNumbers = new Integer[]{4567, -9870, 1234};
 Collections.sort(Arrays.asList(arrayNumbers));
 size = arrayNumbers.length;
 if (size % 2 == 0) {
 assertEquals((long)MathUtil.medianOf(arrayNumbers), ((long)arrayNumbers[size / 2 - 1] + (long)arrayNumbers[size / 2]) / 2);
 } else {
 assertEquals((long)MathUtil.medianOf(arrayNumbers), (long)arrayNumbers[size / 2]);
 }
 }
}