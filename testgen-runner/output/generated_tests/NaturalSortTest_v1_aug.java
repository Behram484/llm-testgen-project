package naturalsort;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class NaturalSortTest {

 @BeforeEach
 void setUp() {}

 @AfterEach
 void tearDown() {}

 @Test
 public void testCompare() {
 assertEquals(-1, NaturalSort.compare("7", "17"));
 assertEquals(0, NaturalSort.compare("7", "7"));
 assertEquals(+1, NaturalSort.compare("17", "7"));
 }

 @Test
 public void testCompareIgnoreCase() {
 assertEquals(-1, NaturalSort.compareIgnoreCase("7", "17"));
 assertEquals(0, NaturalSort.compareIgnoreCase("7", "7"));
 assertEquals(+1, NaturalSort.compareIgnoreCase("17", "7"));
 }

 @Test
 public void testCompare_sameLength() {
 assertThrows(NullPointerException.class, () -> {
 NaturalSort.compare(null, "");
 });
 assertEquals(-1, NaturalSort.compare("a", "b"));
 assertEquals(+1, NaturalSort.compare("b", "a"));
 }
 
 @Test
 public void testCompareIgnoreCase_sameLength() {
 assertThrows(NullPointerException.class, () -> {
 NaturalSort.compareIgnoreCase(null, "");
 });
 assertEquals(-1, NaturalSort.compareIgnoreCase("a", "b"));
 assertEquals(+1, NaturalSort.compareIgnoreCase("b", "a"));
 }
 
 // New tests to target surviving mutants

 @Test
 public void testCompare_differentLength() {
 assertEquals(-1, NaturalSort.compare("7", "70"));
 assertEquals(+1, NaturalSort.compare("70", "7"));
 }
 
 @Test
 public void testCompareIgnoreCase_differentLength() {
 assertEquals(-1, NaturalSort.compareIgnoreCase("7", "70"));
 assertEquals(+1, NaturalSort.compareIgnoreCase("70", "7"));
 }
}