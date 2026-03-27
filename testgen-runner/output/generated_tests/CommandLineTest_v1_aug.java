package commandline;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CommandLineTest {
 private CommandLine cmd;
 
 @BeforeEach
 void setUp() {
 cmd = new CommandLine();
 }

 // Existing tests remain the same

 @Test
 void testAddNewSwitchOrParameterWithOverwriteFalseAndCheckItsPresence() {
 assertTrue(cmd.add("new_switch", null));
 assertFalse(cmd.add("new_switch", "new value", false));
 assertEquals(null, cmd.value("new_switch")); // should still be null since overwrite=false
 }

 @Test
 void testAddNewSwitchOrParameterWithOverwriteTrueAndCheckItsPresence() {
 assertTrue(cmd.add("existing_switch", null));
 assertEquals(null, cmd.value("existing_switch")); // existing value should be null
 
 assertTrue(cmd.add("existing_switch", "new value", true));
 assertEquals("new value", cmd.value("existing_switch")); 
 }

 @Test
 void testAddNewParameterWithDefaultValue() {
 assertEquals("default value", cmd.value("parameter", "default value")); // parameter doesn't exist yet, should return default value
 
 assertTrue(cmd.add("parameter", null)); 
 assertEquals("default value", cmd.value("parameter", "default value")); // parameter still exists but without a value, should return default value
 
 assertTrue(cmd.add("parameter", "actual value"));
 assertEquals("actual value", cmd.value("parameter", "default value")); 
 }
}