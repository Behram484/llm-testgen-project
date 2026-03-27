package stringcomparator;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class StringComparatorTest_v1 {
 private final StringComparator comparator = new StringComparator(); // Create an instance of StringComparator for the tests

 @Test
 public void testCompareObject() {
 Assertions.assertEquals(0, comparator.compare("abc", "abc"));
 Assertions.assertEquals(-1, comparator.compare("abcd", "abcde"));
 Assertions.assertThrows(ClassCastException.class, () -> {
 comparator.compare("abc", 123);
 });
 }

 @Test
 public void testCompareString() {
 Assertions.assertEquals(0, StringComparator.compare("abc", "abc"));
 Assertions.assertEquals(-1, StringComparator.compare("abcd", "abcde"));
 Assertions.assertThrows(ClassCastException.class, () -> {
 StringComparator.compare("abc", 123);
 });
 }

 @Test
 public void testCompareDifferentLength() {
 Assertions.assertEquals(-1, StringComparator.compare("abc", "abcd"));
 Assertions.assertEquals(+1, StringComparator.compare("abcd", "abc"));
 }

 @Test
 public void testCompareIgnoreCase() {
 Assertions.assertEquals(0, StringComparator.compare("ABC", "abc"));
 }
}