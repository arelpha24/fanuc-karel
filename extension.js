const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    // Read the JSON files
    const functionsWithParameters = JSON.parse(fs.readFileSync(path.join(__dirname, 'karelFunctions.json'), 'utf-8'));
    const patterns = JSON.parse(fs.readFileSync(path.join(__dirname, 'karelPatterns.json'), 'utf-8'));

    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider('karel', {
            provideCompletionItems(document, position) {
                // Autocomplete for functions
                const functionCompletionItems = functionsWithParameters.map(func => {
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

                // Autocomplete for patterns
                const patternCompletionItems = patterns.map(pattern => {
                    const item = new vscode.CompletionItem(pattern, vscode.CompletionItemKind.Text);
                    item.insertText = pattern;
                    return item;
                });

                return functionCompletionItems.concat(patternCompletionItems);
            }
        }, '.')); // Trigger completion when '.' is pressed
}
exports.activate = activate;

function deactivate() {}
exports.deactivate = deactivate;
