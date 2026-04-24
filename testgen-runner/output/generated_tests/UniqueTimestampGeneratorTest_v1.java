package dk.statsbiblioteket.summa.common.util;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class UniqueTimestampGeneratorTest_v1 {
 private UniqueTimestampGenerator cut; // Cut stands for Component Under[5D[K
Under Test

 @BeforeEach
 public void setUp() {
 cut = new UniqueTimestampGenerator();
 }

 @Test
 public void testNextGeneratesUniqueTimestampsInSortedOrder() {
 long timestamp1 = cut.next();
 long timestamp2 = cut.next();
 
 assertTrue(timestamp1 < timestamp2);
 }
 
 @Test
 public void testSystemTimeExtractsCorrectSystemTimeFromTimestamp() {
 long systemTime = System.currentTimeMillis();
 long timestamp = cut.next(systemTime);
 
 assertEquals(systemTime, cut.systemTime(timestamp));
 }
 
 @Test
 public void testSaltExtractsCorrectSaltFromTimestamp() {
 long systemTime = System.currentTimeMillis();
 long timestamp1 = cut.next(systemTime);
 long timestamp2 = cut.next(systemTime + 1); // Different system tim[3D[K
time to ensure salt is unique
 
 assertNotEquals(cut.salt(timestamp1), cut.salt(timestamp2));
 }
 
 @Test
 public void testBaseTimestampGeneratesCorrectBaseTimestamp() {
 long systemTime = System.currentTimeMillis();
 long timestamp = cut.next(systemTime);
 
 assertEquals((systemTime << UniqueTimestampGenerator.SALT_BITS), cu[2D[K
cut.baseTimestamp(timestamp));
 }
 
 @Test
 public void testFormatTimestampFormatsCorrectly() {
 long systemTime = System.currentTimeMillis();
 String expected = new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:m[45D[K
java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS").format(new java.uti[8D[K
java.util.Date(systemTime));
 
 assertEquals(expected, cut.formatSystemTime(systemTime));
 }
 
 @Test
 public void testParseSystemTimeParsesCorrectly() throws Exception {
 long systemTime = System.currentTimeMillis();
 String formattedTime = cut.formatSystemTime(systemTime);
 
 assertEquals(systemTime, cut.parseSystemTime(formattedTime));
 }
}