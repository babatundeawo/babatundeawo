# Publishing and maintenance guide

For the owner of this repository. Everything below is done on the GitHub website. No terminal and nothing to install.

## How this repository goes live

This is your **profile repository**: GitHub shows its `README.md` at <https://github.com/babatundeawo>. There is nothing to build or deploy and no GitHub Pages setting to switch on. The moment a change reaches the `main` branch, your profile shows it.

Three small automatic jobs run in the background (see the **Actions** tab):

| Job | What it does | When |
| --- | --- | --- |
| **Update profile stats** | Refreshes the "GitHub at a glance" cards from your public repositories. | Every Monday, and when you press **Run workflow** |
| **CodeQL** | Scans the one small script in the repository for security problems. | On changes to `main`, and weekly |
| **Check links** | Looks for broken links in the README and these guides and reports them in the run log. | When a pull request changes them, and monthly |

## Publish the redesign safely (one time)

The redesign is delivered as a ready-made set of files. Your live profile does not change until you merge it.

1. Open <https://github.com/babatundeawo/babatundeawo> and click **Add file → Upload files**.
2. Drag in the **contents** of the delivered folder (the files and folders inside it: `README.md`, `assets`, `docs`, `.github`), not the folder itself. If your computer hides the `.github` folder, see "Folder `.github` is hidden" below.
3. At the bottom, choose **Create a new branch for this commit**, name it `rebrand/premium-redesign`, and click **Propose changes**.
4. On the next page click **Create pull request**, then **Create pull request** again. Your live profile is still unchanged.
5. To preview: on the pull request click the **Files changed** tab, open `README.md` and click the three dots (**⋯**) → **View file**. GitHub shows it exactly as visitors will see it.
6. Happy with it? Click **Merge pull request → Confirm merge**. Your profile updates within a minute. Not happy? Click **Close pull request**. Nothing changes.
7. After merging, open the **Actions** tab, choose **Update profile stats** on the left, click **Run workflow → Run workflow**, and wait for a green tick. The stat card then shows real numbers.

**Folder `.github` is hidden.** On a Mac press **Cmd + Shift + .** in Finder; on Windows open **View → Show → Hidden items** in File Explorer. Alternatively create the files with **Add file → Create new file** and type `.github/workflows/update-stats.yml` as the name (typing the slash creates the folder), then paste the content.

## Editing your profile later

1. Open `README.md` in the repository and click the pencil icon (**Edit this file**).
2. Make your change, click **Commit changes…**, and commit directly to `main` for small edits, or choose a new branch and a pull request for larger ones.
3. Open your profile page and refresh to see it.

For colours, banner text and images see [CUSTOMIZING.md](CUSTOMIZING.md).

## Check that a background job worked

1. Click the **Actions** tab.
2. Click a run in the list. A **green tick** means success. A **red cross** means a problem.
3. For a red cross, click the run, then the failed job (marked with a red cross), then the failed step. The error text is at the bottom of the step.

Common cases:

- **Update profile stats fails with "Permission denied" or "403"**: open **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, click **Save**, then run the job again.
- **Update profile stats says it left the cards unchanged**: GitHub could not be reached that minute. Run it again later; the old cards stay in place meanwhile.
- **Check links shows broken links**: this job only reports. Open the run log, find the listed address, and update or remove that link in `README.md`.

## Go back to an earlier version

Every change is saved in history, so nothing is lost.

- **Undo a whole merged change:** open **Pull requests → Closed**, open the merged pull request, click **Revert**, then **Create pull request** and merge it.
- **Restore one file:** open the file, click **History**, open the older version you want, click the three dots (**⋯**) → **View file**, click **Raw** copy the text, then edit the current file and paste it over.

## Optional safety switches

In the repository, open **Settings → Code security** (called **Advanced Security** in some accounts) and turn on:

- **Dependabot alerts** and **Dependabot security updates**. GitHub then warns you about outdated tools. `dependabot.yml` already keeps the automation versions current with a monthly pull request.
- **Secret scanning** and **Push protection**. GitHub then blocks a commit that contains a password or key.

These need no setup beyond clicking **Enable**. Never paste passwords, tokens or private keys into any file in this repository.

## About the stat card

The card counts public repositories, stars and primary languages across `babatundeawo`, `techbaseng`, `kbischool` and `rccgkd`, skipping forks and archived repositories. Private repositories are never read or shown. To change which accounts are counted, edit the `ACCOUNTS` list near the top of `.github/scripts/generate_stats.py`.
