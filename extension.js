const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    // Read the JSON file
    const functionsWithParameters = JSON.parse(fs.readFileSync(path.join(__dirname, 'karelFunctions.json'), 'utf-8'));

    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider('karel', {
            provideCompletionItems(document, position) {
                const completionItems = functionsWithParameters.map(func => {
                    const item = new vscode.CompletionItem(func.name, vscode.CompletionItemKind.Function);

                    // Prepare the detail string and the function call with placeholders for the parameters
                    const detailParts = [];
                    const snippet = new vscode.SnippetString();
                    snippet.appendText(`${func.name}(`);
                    func.parameters.forEach((parameter, index) => {
                        detailParts.push(`${parameter.name}: ${parameter.type}`);
                        snippet.appendPlaceholder(parameter.name);
                        if (index !== func.parameters.length - 1) {
                            snippet.appendText(', ');
                        }
                    });
                    snippet.appendText(')');
                    item.detail = `${func.name}(${detailParts.join(', ')})`;
                    item.insertText = snippet;
                    
                    return item;
                });

                return completionItems;
            }
        }, '.')); // Trigger completion when '.' is pressed
}
exports.activate = activate;

function deactivate() {}
exports.deactivate = deactivate;
