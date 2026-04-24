package net.sourceforge.squirrel_sql.client.session.schemainfo;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class FilterMatcherTest_v1 {
 private FilterMatcher filterMatcher;

 @BeforeEach
 void setUp() {
 // Arrange
 filterMatcher = new FilterMatcher("Geer%", null);
 }

 @Test
 void testMatchesMethodWithMatchingNameReturnsTrue() {
 // Act and Assert
 assertEquals(false, filterMatcher.matches("Gerhard"));
 }

 @Test
 void testMatchesMethodWithoutMatchingNameReturnsFalse() {
 // Act and Assert
 assertEquals(false, filterMatcher.matches("Alice"));
 }
}