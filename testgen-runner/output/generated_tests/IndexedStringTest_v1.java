package de.beiri22.stringincrementor.helper;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class IndexedStringTest_v1 {
 @Test
 public void testIndexOf() {
 // Create a new instance of the IndexedString with string "hello"
 IndexedString indexedString = new IndexedString("hello");

 // Test if 'indexOf' returns correct index for target string "ll"
 char[] target1 = {'l', 'l'};
 Assertions.assertEquals(2, indexedString.indexOf(target1));

 // Test if 'indexOf' returns -1 when the target string is not found
 char[] target2 = {'x', 'y', 'z'};
 Assertions.assertEquals(-1, indexedString.indexOf(target2));
 }

 @Test
 public void testIndexOfWithEmptyTarget() {
 // Create a new instance of the IndexedString with string "hello"
 IndexedString indexedString = new IndexedString("hello");

 // Test if 'indexOf' returns 0 when the target is an empty character ar[2D[K
array
 char[] target = {};
 Assertions.assertEquals(0, indexedString.indexOf(target));
 }
}