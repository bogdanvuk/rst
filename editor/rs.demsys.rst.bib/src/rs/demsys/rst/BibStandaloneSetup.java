/*
 * generated by Xtext
 */
package rs.demsys.rst;

/**
 * Initialization support for running Xtext languages 
 * without equinox extension registry
 */
public class BibStandaloneSetup extends BibStandaloneSetupGenerated{

	public static void doSetup() {
		new BibStandaloneSetup().createInjectorAndDoEMFRegistration();
	}
}

