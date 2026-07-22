# Valkey PR Health Report

**Generated:** 2026-07-22 08:27 UTC | **Repo:** [valkey-io/valkey](https://github.com/valkey-io/valkey)

---

## 📊 By the Numbers

| Metric | Count |
|--------|-------|
| Total open PRs | 303 |
| Non-draft | 277 |
| Draft | 26 |
| Bot PRs (backports etc.) | 4 |
| `major-decision-pending` | 35 |
| `major-decision-approved` | 9 |
| `major-decision-deferred` | 3 |
| `to-be-merged` | 4 |
| `to-be-closed` | 1 |
| `stalled` | 2 |
| `run-extra-tests` | 14 |
| `needs-doc-pr` | 5 |


## ⚡ Immediate Actions


### Merge Now (`to-be-merged`)

| PR | Title | Author | Age | Last update |
|----|-------|--------|-----|-------------|
| [3413](https://github.com/valkey-io/valkey/pull/3413) | Optimize infoCommand with SDS pre-allocation | charsyam | 3mo old | 3mo ago |
| [3465](https://github.com/valkey-io/valkey/pull/3465) | fix: update maxmemory test to account for SDS pre-allocation memory | djk1027 | 3mo old | 13d ago |
| [3491](https://github.com/valkey-io/valkey/pull/3491) | zset: add in-place fast path for score updates in listpack encoding | charsyam | 3mo old | 11d ago |
| [3810](https://github.com/valkey-io/valkey/pull/3810) | Fix zrangebyscore empty exclusive bound | chenshi5012 | 2mo old | 2d ago |


### Community-Approved, Awaiting Merge (`major-decision-approved`)

_Decision is made — these just need someone to merge them._

| PR | Title | Author | Age | Last update |
|----|-------|--------|-----|-------------|
| [685](https://github.com/valkey-io/valkey/pull/685) | Align the entry read and lag rules of the consumer group | artikell | 2.1y old | 7w ago |
| [866](https://github.com/valkey-io/valkey/pull/866) | New maxmemory-scripts config to limit all cached scripts (EVAL and SCR… | enjoy-binbin | 2.0y old | 7w ago |
| [2555](https://github.com/valkey-io/valkey/pull/2555) | Use BIO thread for cluster config saving in cluster-config-save-behavi… | enjoy-binbin | 10mo old | 2mo ago |
| [2972](https://github.com/valkey-io/valkey/pull/2972) | Add an optional parameter to SISMEMBER; return -1 if the key does not… | li-benson | 6mo old | 6mo ago |
| [2978](https://github.com/valkey-io/valkey/pull/2978) | Add XX option to ZRANGE commands for null/empty distinction | youngmore1024 | 6mo old | 0d ago |
| [3253](https://github.com/valkey-io/valkey/pull/3253) | Add NX,XX,EX,PX support to INCR, INCRBY, INCRBYFLOAT, DECR, DECRBY com… | GavinDmello | 4mo old | 0d ago |
| [3466](https://github.com/valkey-io/valkey/pull/3466) | XACKDEL Command | nickiaq | 3mo old | 1d ago |
| [3467](https://github.com/valkey-io/valkey/pull/3467) | XDELEX Command | nickiaq | 3mo old | 1d ago |
| [3522](https://github.com/valkey-io/valkey/pull/3522) | Fail fast on empty CA directory at TLS config load | yang-z-o | 3mo old | 2mo ago |


### Close Now

| PR | Title | Author | Age | Reason |
|----|-------|--------|-----|--------|
| [3427](https://github.com/valkey-io/valkey/pull/3427) | Windows native builds & tests (Microsoft Visual Studio 2026) | SamuelMarks | 3mo | `to-be-closed` |
| [3558](https://github.com/valkey-io/valkey/pull/3558) | hash: harden HRANDFIELD against expired-heavy hashes | charsyam | 2mo | `stalled` |
| [974](https://github.com/valkey-io/valkey/pull/974) | Fix data loss when the old primary takes over the slots afte | enjoy-binbin | 1.9y | `stalled` |


## 🟡 Decision Bottleneck (`major-decision-pending`)

**33 PRs** blocked waiting for a community vote.

| PR | Title | Author | Age | Last update |
|----|-------|--------|-----|-------------|
| [962](https://github.com/valkey-io/valkey/pull/962) | Add command "Client Capa subv2" to change behavior for SUBSCRIBE and S… | hwware | 1.9y old | 7w ago |
| [978](https://github.com/valkey-io/valkey/pull/978) | Add last_fork_start_time to INFO STATS | enjoy-binbin | 1.9y old | 3mo ago |
| [1151](https://github.com/valkey-io/valkey/pull/1151) | Adding KEYINFO command to find out keys that have large number of elem… | otheng03 | 1.8y old | 7w ago |
| [1418](https://github.com/valkey-io/valkey/pull/1418) | Add new SCRIPT STATS subcommand | artikell | 1.6y old | 1.4y ago |
| [1672](https://github.com/valkey-io/valkey/pull/1672) | Implementation of write throttling | lschmidtcavalcante-sc | 1.5y old | 6mo ago |
| [1964](https://github.com/valkey-io/valkey/pull/1964) | Add sentinel failover SAFE option | li-benson | 1.3y old | 7w ago |
| [2157](https://github.com/valkey-io/valkey/pull/2157) | Kill the busy script during failover to avoid data inconsistency | enjoy-binbin | 1.1y old | 5mo ago |
| [2204](https://github.com/valkey-io/valkey/pull/2204) | Add cluster-replica-priority to allow better ranking in auto failover | enjoy-binbin | 1.1y old | 0d ago |
| [2275](https://github.com/valkey-io/valkey/pull/2275) | Add keyspace-hits and keyspace-misses metrics under CLUSTER SLOT-STATS… | enjoy-binbin | 1.1y old | 3mo ago |
| [2331](https://github.com/valkey-io/valkey/pull/2331) | Adding support for DumpSerializedValue API | cdorantes05 | 1.0y old | 3mo ago |
| [2368](https://github.com/valkey-io/valkey/pull/2368) | add parameter for initiating bgrewriteaof on exceeding threshold AOF s… | kronwerk | 1.0y old | 0d ago |
| [2385](https://github.com/valkey-io/valkey/pull/2385) | Allow dynamic modification of databases num if the db is not been used | enjoy-binbin | 11mo old | 5w ago |
| [2586](https://github.com/valkey-io/valkey/pull/2586) | Fix two primaries scenario due to unknown shard_id | deepakrn | 10mo old | 4mo ago |
| [2689](https://github.com/valkey-io/valkey/pull/2689) | Fix #2678 don't add loadmodule when from config | remicollet | 9mo old | 7w ago |
| [2891](https://github.com/valkey-io/valkey/pull/2891) | Reset prefetch and ACL stats via CONFIG RESETSTAT | enjoy-binbin | 7mo old | 0d ago |
| [2971](https://github.com/valkey-io/valkey/pull/2971) | Add used_memory_overhead_human and used_memory_dataset_human info fiel… | enjoy-binbin | 7mo old | 6mo ago |
| [2979](https://github.com/valkey-io/valkey/pull/2979) | Add VM_AddCommandACLCategories API to assign ACL categories to existin… | bandalgomsu | 6mo old | 6mo ago |
| [2990](https://github.com/valkey-io/valkey/pull/2990) | Avoid loading keys for unowned slots | ranshid | 6mo old | 4mo ago |
| [3068](https://github.com/valkey-io/valkey/pull/3068) | Cleanup around FAST command flag | enjoy-binbin | 6mo old | 3w ago |
| [3191](https://github.com/valkey-io/valkey/pull/3191) | Runtime Payload Histogram Tracking | YiwenZhang12 | 5mo old | 2w ago |
| … | *13 more* | | | |


## 🧑‍💻 Top Contributors by Open PR Count

| Author | Open PRs |
|--------|----------|
| [enjoy-binbin](https://github.com/enjoy-binbin) | 23 🚨 |
| [jsoref](https://github.com/jsoref) | 14 🚨 |
| [quanyeyang](https://github.com/quanyeyang) | 8 🚨 |
| [rainsupreme](https://github.com/rainsupreme) | 8 🚨 |
| [charsyam](https://github.com/charsyam) | 8 🚨 |
| [bandalgomsu](https://github.com/bandalgomsu) | 6 ⚠️ |
| [satheeshaGowda](https://github.com/satheeshaGowda) | 5 ⚠️ |
| [AlisinaDevelo](https://github.com/AlisinaDevelo) | 5 ⚠️ |
| [omerrubi-amzn](https://github.com/omerrubi-amzn) | 5 ⚠️ |
| [magic-peach](https://github.com/magic-peach) | 4 |
| [sarthakaggarwal97](https://github.com/sarthakaggarwal97) | 4 |
| [cjx-zar](https://github.com/cjx-zar) | 4 |
| [hpatro](https://github.com/hpatro) | 4 |
| [artikell](https://github.com/artikell) | 4 |
| [YiwenZhang12](https://github.com/YiwenZhang12) | 4 |


## 🕰 Long-Dormant PRs (90+ days since last update)

**88 non-draft PRs** haven't been updated in 90+ days.

| PR | Title | Author | Created | Last update |
|----|-------|--------|---------|-------------|
| [1547](https://github.com/valkey-io/valkey/pull/1547) | feat: stats and keyspace notifications about lazy expiration | proost | 1.5y old | 1.4y ago |
| [1418](https://github.com/valkey-io/valkey/pull/1418) | Add new SCRIPT STATS subcommand | artikell | 1.6y old | 1.4y ago |
| [1284](https://github.com/valkey-io/valkey/pull/1284) | fix: readonly client moved inconsistency | proost | 1.7y old | 1.4y ago |
| [906](https://github.com/valkey-io/valkey/pull/906) | Keep the log fd, don't re-open logfile in every logs | enjoy-binbin | 1.9y old | 1.4y ago |
| [363](https://github.com/valkey-io/valkey/pull/363) | Add support for compiling with mimalloc  | WM0323 | 2.2y old | 1.4y ago |
| [1689](https://github.com/valkey-io/valkey/pull/1689) | Implementation of CPU throttling | lschmidtcavalcante-sc | 1.4y old | 1.4y ago |
| [1120](https://github.com/valkey-io/valkey/pull/1120) | Add admin-port to let administrator connect to the server even maxclie… | hwware | 1.8y old | 1.3y ago |
| [1909](https://github.com/valkey-io/valkey/pull/1909) | Add cluster-non-random-gosip option | VyacheslavVanin | 1.3y old | 1.3y ago |
| [2183](https://github.com/valkey-io/valkey/pull/2183) | Spelling | jsoref | 1.1y old | 1.1y ago |
| [2238](https://github.com/valkey-io/valkey/pull/2238) | spelling: ; otherwise, | jsoref | 1.1y old | 1.1y ago |
| [2242](https://github.com/valkey-io/valkey/pull/2242) | spelling: cannot | jsoref | 1.1y old | 1.1y ago |
| [2250](https://github.com/valkey-io/valkey/pull/2250) | Spelling 14 | jsoref | 1.1y old | 1.1y ago |
| [2248](https://github.com/valkey-io/valkey/pull/2248) | spelling: otherwise, | jsoref | 1.1y old | 1.1y ago |
| [2306](https://github.com/valkey-io/valkey/pull/2306) | Unexpected variable overriding from .make-settings file | yzc-yzc | 1.0y old | 1.0y ago |
| [2318](https://github.com/valkey-io/valkey/pull/2318) | change check order for xautoclaim | charsyam | 1.0y old | 1.0y ago |
| [2247](https://github.com/valkey-io/valkey/pull/2247) | spelling: nonexistent | jsoref | 1.1y old | 11mo ago |
| [2239](https://github.com/valkey-io/valkey/pull/2239) | Spelling 2 | jsoref | 1.1y old | 11mo ago |
| [2551](https://github.com/valkey-io/valkey/pull/2551) | Roll backward downgrade compatibility from Redis 7.2 and Valkey 7.2/8.… | satheeshaGowda | 10mo old | 10mo ago |
| [2575](https://github.com/valkey-io/valkey/pull/2575) | valkey-benchmark: Tests for ZSCORE, ZRANGE and SISMEMBER | ranshid | 10mo old | 10mo ago |
| [2496](https://github.com/valkey-io/valkey/pull/2496) | Add static specifier to the internal functions of HLL | yzc-yzc | 11mo old | 8mo ago |
| [2795](https://github.com/valkey-io/valkey/pull/2795) | updated modules examples to compile on Valkey 7.2 branch | dmitrypol | 8mo old | 8mo ago |
| [2255](https://github.com/valkey-io/valkey/pull/2255) | Accept socket judge fd overflow | kukey | 1.1y old | 7mo ago |
| [1455](https://github.com/valkey-io/valkey/pull/1455) | Add GETPXT, MGETPXT (Get with millisecond expiration) commands | arcivanov | 1.6y old | 7mo ago |
| [2979](https://github.com/valkey-io/valkey/pull/2979) | Add VM_AddCommandACLCategories API to assign ACL categories to existin… | bandalgomsu | 6mo old | 6mo ago |
| [2972](https://github.com/valkey-io/valkey/pull/2972) | Add an optional parameter to SISMEMBER; return -1 if the key does not… | li-benson | 6mo old | 6mo ago |
| … | *63 more* | | | |


## 🔥 Open Deflake / Test-Fix PRs

_Merging these reduces CI noise for everyone._

| PR | Title | Author | Age | Last update |
|----|-------|--------|-----|-------------|
| [3049](https://github.com/valkey-io/valkey/pull/3049) | Fix flaky test in manual-failover.tcl | Nikhil-Manglore | 6mo old | 3mo ago |
| [4102](https://github.com/valkey-io/valkey/pull/4102) | Deflake "Replica output bytes metric" with atomic stats capture | Taeknology | 2w old | 0d ago |
| [4179](https://github.com/valkey-io/valkey/pull/4179) | Deflake: replace flaky wall-clock defrag latency assertion with determ… | rainsupreme | 6d old | 0d ago |
| [4223](https://github.com/valkey-io/valkey/pull/4223) | Deflake ccov: Contain slot migration test failures with a recovery bar… | rainsupreme | 1d old | 0d ago |
| [4251](https://github.com/valkey-io/valkey/pull/4251) | deflake ccov: Use _exit() when a child is killed by SIGUSR1 | rainsupreme | 0d old | 0d ago |


## ⏱ High CI Burden (`run-extra-tests`)

**13 PRs** trigger extended CI runs.

| PR | Title | Author | Age |
|----|-------|--------|-----|
| [866](https://github.com/valkey-io/valkey/pull/866) | New maxmemory-scripts config to limit all cached scripts (EV | enjoy-binbin | 2.0y |
| [2204](https://github.com/valkey-io/valkey/pull/2204) | Add cluster-replica-priority to allow better ranking in auto | enjoy-binbin | 1.1y |
| [2279](https://github.com/valkey-io/valkey/pull/2279) | The smaller config epoch primary will become the replica whe | enjoy-binbin | 1.1y |
| [2555](https://github.com/valkey-io/valkey/pull/2555) | Use BIO thread for cluster config saving in cluster-config-s | enjoy-binbin | 10mo |
| [3335](https://github.com/valkey-io/valkey/pull/3335) | Fix RDMA re-entrancy assertion and lost wakeup deadlocks wit | quanyeyang | 4mo |
| [3468](https://github.com/valkey-io/valkey/pull/3468) | Ignore stale replica messages for failed primaries | sarthakaggarwal97 | 3mo |
| [3589](https://github.com/valkey-io/valkey/pull/3589) | ci: Add slow tag to fuzzer and expand libc-malloc CI to run  | jjuleslasarte | 2mo |
| [3717](https://github.com/valkey-io/valkey/pull/3717) | Add support for secondary certificates | pkhartsk | 2mo |
| [3833](https://github.com/valkey-io/valkey/pull/3833) | Speed up split-vote elections with the new FAILOVER_AUTH_NAC | enjoy-binbin | 8w |
| [3853](https://github.com/valkey-io/valkey/pull/3853) | Streaming Compression support for Replication | roshkhatri | 7w |
| [4140](https://github.com/valkey-io/valkey/pull/4140) | Retry PSYNC on -BUSY error instead of downgrading to SYNC | enjoy-binbin | 11d |
| [4152](https://github.com/valkey-io/valkey/pull/4152) | Account for deferred client frees during eviction | dhruv2x | 9d |
| [4171](https://github.com/valkey-io/valkey/pull/4171) | Fix ping_sent getting stuck when peer traffic keeps link ali | enjoy-binbin | 6d |

---

*Report generated by [valkey-pr-watchtower](https://github.com/valkey-rainfall/valkey-pr-watchtower). Data from GitHub API. Opinions are the author's own.*