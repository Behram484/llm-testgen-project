package commandline;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CommandLineTest_v1 {
 private CommandLine cmd;
 
 @BeforeEach
 void setUp() {
 cmd = new CommandLine();
 }

 @Test
 void testExistsForNonExistentOptionAndParameter() {
 assertFalse(cmd.exists("non-existent"));
 }

 @Test
 void testIsSwitchForExistingSwitch() {
 cmd.add("-switch", null);
 assertTrue(cmd.isSwitch("-switch"));
 }

 @Test
 void testIsParameterForExistingParameter() {
 cmd.add("parameter", "value");
 assertTrue(cmd.isParameter("parameter"));
 }

 @Test
 void testValueReturnDefaultValueForNonExistentOptionOrParameter() {
 assertEquals("default", cmd.value("non-existent", "default"));
 }

 @Test
 void testAddNewSwitchOrParameterAndCheckItsPresence() {
 assertTrue(cmd.add("new_switch", null));
 assertTrue(cmd.exists("new_switch"));
 
 assertTrue(cmd.add("parameter", "value"));
 assertEquals("value", cmd.value("parameter"));
 }
}