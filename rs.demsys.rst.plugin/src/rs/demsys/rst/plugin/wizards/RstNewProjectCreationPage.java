package rs.demsys.rst.plugin.wizards;

import org.eclipse.jface.dialogs.Dialog;
import org.eclipse.jface.util.BidiUtils;
import org.eclipse.swt.SWT;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Text;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.dialogs.WizardNewProjectCreationPage;
import org.eclipse.ui.internal.ide.IDEWorkbenchMessages;
import org.eclipse.ui.internal.ide.IIDEHelpContextIds;
import org.eclipse.ui.internal.ide.dialogs.ProjectContentsLocationArea;

public class RstNewProjectCreationPage extends WizardNewProjectCreationPage {

	private String initialAuthorFieldValue;
	
	Text authorNameField;
	Text versionField;	
	
    // constants
    private static final int SIZING_TEXT_FIELD_WIDTH = 250;
	
    public RstNewProjectCreationPage(String pageName) {
    	super(pageName);
    }
    
    public void createControl(Composite parent) {
    	super.createControl(parent);
    	Composite control = (Composite) getControl();
    	
    	// project specification group
        Composite settingsGroup = new Composite(control, SWT.NONE);
        GridLayout layout = new GridLayout();
        layout.numColumns = 2;
        settingsGroup.setLayout(layout);
        settingsGroup.setLayoutData(new GridData(GridData.FILL_HORIZONTAL));
    	
    	setInitialAuthortName(System.getProperty("user.name"));
    	authorNameField = addFieldToGroup(settingsGroup, "Author Name", initialAuthorFieldValue);
    	versionField = addFieldToGroup(settingsGroup, "Document Version", "1.0.0");
    }
    
    private final Text addFieldToGroup(Composite parent, String labelName, String initValue)
    {
        // new project label
        Label authorLabel = new Label(parent, SWT.NONE);
        authorLabel.setText(labelName);
        authorLabel.setFont(parent.getFont());

        // new project name entry field
        Text widget = new Text(parent, SWT.BORDER);
        GridData data = new GridData(GridData.FILL_HORIZONTAL);
        data.widthHint = SIZING_TEXT_FIELD_WIDTH;
        widget.setLayoutData(data);
        widget.setFont(parent.getFont());

        // Set the initial value first before listener
        // to avoid handling an event during the creation.
        if (initValue != null) {
        	widget.setText(initValue);
		}
        BidiUtils.applyBidiProcessing(widget, BidiUtils.BTD_DEFAULT);
        
        return widget;
    }
    
    private final void createVersionNameGroup(Composite parent) {
        // project specification group
        Composite authorGroup = new Composite(parent, SWT.NONE);
        GridLayout layout = new GridLayout();
        layout.numColumns = 2;
        authorGroup.setLayout(layout);
        authorGroup.setLayoutData(new GridData(GridData.FILL_HORIZONTAL));

        // new project label
        Label authorLabel = new Label(authorGroup, SWT.NONE);
        authorLabel.setText("Author Name");
        authorLabel.setFont(parent.getFont());

        // new project name entry field
        authorNameField = new Text(authorGroup, SWT.BORDER);
        GridData data = new GridData(GridData.FILL_HORIZONTAL);
        data.widthHint = SIZING_TEXT_FIELD_WIDTH;
        authorNameField.setLayoutData(data);
        authorNameField.setFont(parent.getFont());

        // Set the initial value first before listener
        // to avoid handling an event during the creation.
        if (initialAuthorFieldValue != null) {
        	authorNameField.setText(initialAuthorFieldValue);
		}
        BidiUtils.applyBidiProcessing(authorNameField, BidiUtils.BTD_DEFAULT);
    }
    
    public void setInitialAuthortName(String name) {
        if (name == null) {
			initialAuthorFieldValue = null;
		} else {
			initialAuthorFieldValue = name.trim();
        }
    }
    
    public String getAuthorName() {
        if (authorNameField == null) {
			return ""; //$NON-NLS-1$
		}

        return authorNameField.getText().trim();
    }
    
    public String getVersion() {
        if (versionField == null) {
			return ""; //$NON-NLS-1$
		}

        return versionField.getText().trim();
    }
	
}
