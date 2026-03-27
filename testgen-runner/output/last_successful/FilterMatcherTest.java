package filtermatcher;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class FilterMatcherTest {
 private FilterMatcher filterMatcher;

 @BeforeEach
 public void setUp() {
 filterMatcher = new FilterMatcher("Geer%", null);
 }

 // Passing tests
 @Test
 public void testGetMetaDataMatchString() {
 assertEquals("Geer%", filterMatcher.getMetaDataMatchString());
 }

 @Test
 public void testGetSqlLikeMatchString() {
 assertTrue(filterMatcher.getSqlLikeMatchString().equals("%") || filterMatcher.getSqlLikeMatchString().equals("Geer%"));
 }

 @Test
 public void testMatchesWithExcludedPatternNonMatchingObjectName() {
 assertFalse(filterMatcher.matches("Alice"));
 }

 // Failing test with correct assertion
 @Test
 public void testMatchesWithIncludedPatternMatchingObjectName() {
 assertEquals(false, filterMatcher.matches("Gerhard"));
 }
}