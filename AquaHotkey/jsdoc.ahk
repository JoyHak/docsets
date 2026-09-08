```ahk
/**
 * @config
 * 
 * Marker class that deactivates {@link AquaHotkey_Assertions assertions}
 * through the `.Assert()` method. This allows you to add validation to your
 * code while prototyping and debugging, and then remove these checks for
 * better performance after you've gained confidence that your code behaves
 * correctly. The global `Assert()` function still works as previously.
 * 
 * @module  <cfg/DisableAssertions>
 * @author  0w0Demonic
 * @see     https://www.github.com/0w0Demonic/AquaHotkey
 * @see {@link AquaHotkey_Assertions}
 * @example
 * #Include <AquaHotkey>
 * #Include <AquaHotkey\src\cfg\DisableAssertions>
 * 
 * ; immediately returns `Value` without performing any validation
 * Value.Assert(SomethingExpensive)
 */

/**
 * @config
 * 
 * A marker class that disables the type checking done by generic collection
 * types like {@link GenericArray} and {@link GenericMap}.
 * 
 * This can improve performance significantly. You can choose to use
 * type-checked generic collections to catch type errors early during
 * development, and then switch off type-checks after asserting that your
 * code is working correctly.
 * 
 * @module  <cfg/DisableGenerics>
 * @author  0w0Demonic
 * @see     https://www.github.com/0w0Demonic/AquaHotkey
 * @example
 * #Include <AquaHotkeyX>
 * #Include <AquaHotkey/cfg/DisableGenerics>
 * 
 * ; same code as before, but without type checks. The resulting type ends
 * ; up being just plain old `Array`.
 * Grid := Integer[][](
 *     Integer[](1, 2, 3),
 *     Integer[](4, 5, 6)
 * )
 * 
 * LinkedList.OfType(Numeric)  ; --> class LinkedList
 */
/**
 * Introduces an interface for imposing the natural order between values of
 * the same type. This is useful for sorting arrays and other collections.
 * 
 * This feature is exposed via the `.Compare()` method, which is implemented
 * for some of the built-in types like `String`, `Number` and `Array`.
 * 
 * ---
 * 
 * Any type that defines `.Compare()` is considered *comparable*, which
 * grants the following advantages:
 * 
 * - arrays are sortable without a custom {@link Comparator};
 * - instances of that type can be used as key inside an ordered
 *   collection such as {@link SkipListMap} or {@link SkipListSet};
 * - access to ordering functions such as `.Gt()` and `.Lt()`.
 * 
 * ```ahk
 * Arr := ["pear", "banana", "apple", "dragonfruit"]
 * Arr.Sort() ; ["apple", "banana", "dragonfruit", "pear"]
 * 
 * ; --> ["bar", "baz", "foo", "qux"]
 * SkipListSet("foo", "bar", "baz", "qux").ToArray()
 * ```
 * 
 * ---
 * 
 * The `.Compare()` method must adhere to the following rules:
 * 
 * - takes one parameter `Other`, which is *strictly* the same type as `this`.
 *   this also forbids type coercion like `"123"` (string) into `123` (number);
 * - `Other` is a mandatory parameter and not allowed to be `unset`;
 * - returns...
 *    - a negative integer, if `this < Other`;
 *    - `0`, if `this == Other`;
 *    - a positive integer, if `this > Other`.
 * 
 * It is **strongly** recommended - but not mandatory - that if
 * `A.Compare(B) == 0`, then `A.Eq(B)` (see {@link AquaHotkey_Eq `.Eq()`}).
 * Otherwise, sorted sets or maps might behave "strangely", because they are
 * defined in terms of `.Eq()`.
 * 
 * ---
 * 
 * To ensure both values are instances of a type `T`, you can use
 * `T.Compare(A, B)`. This asserts that both `A` and `B` are instances of the
 * calling class `T`.
 * 
 * In the example above, the return statement can be rewritten to assert that
 * all three fields are `Integer`s:
 * 
 * ```ahk
 * return Integer.Compare(this.Major, Other.Major)
 *     || Integer.Compare(this.Minor, Other.Minor)
 *     || Integer.Compare(this.Patch, Other.Patch)
 * ```
 * 
 * Because {@link AquaHotkey_DuckTypes duck types} might not necessarily
 * inherit the proper `.Compare()` method, you must implement a custom
 * `static Compare()` for the duck type. These overrides should use
 * {@link AquaHotkey_DuckTypes.Any#Is `.Is()`} for type-checking.
 * 
 * Lastly, `*ClassObject*.Compare` returns a {@link Comparator} which can be
 * conveniently used as configuration inside ordered collections, or as
 * parameter for `.Sort()` methods. `Any.Compare` is type-agnostic, meaning
 * "use any natural ordering, if present".
 * 
 * ```ahk
 * Arr := ["24.2", 45, 0, "0", 22.0, "-3"]
 * 
 * ; e.g.: ("0", 0) => (true).Compare(false) => 1.Compare(0) => 1
 * NumbersFirst(A, B) => (A is String).Compare(B is String)
 * 
 * Arr.Sort( (Numeric.Compare).Then(NumbersFirst) )
 * ; -> ["-3", 0, "0", 22.0, "24.2", 45]
 * ;           ^ (number zero comes before string zero)
 * ```
 * 
 * @module  <Base/Comparable>
 * @author  0w0Demonic
 * @see     https://www.github.com/0w0Demonic/AquaHotkey
 * @see {@link Comparator}
 * @see {@link SkipListMap}
 * @see {@link SkipListSet}
 * @see {@link AquaHotkey_DuckTypes duck types}
 * @see {@link AquaHotkey_Eq `.Eq()`}
 * @example
 * ; result: [1.98, 23, 123, 3455]
 * Array(123, 23, 1.98, 3455).Sort()
 * 
 * ; -1 (implies "smaller", i.e. `-1 < 2`)
 * Number.Compare(-1, 2)
 * 
 * ; TypeError! Expected an String.
 * "123".Compare(123)
 * 
 * ; TypeError! Expected an Array.
 * Array.Compare(1, 2)
 */ 
/**
 * Finds and returns the first element to match the given condition.
 * If an element was found, the method returns `true`, otherwise
 * `false`.
 * 
 * @param   {VarRef<Any?>}            Output     output value
 * @param   {(Any, Any*) => Boolean}  Condition  the given condition
 * @param   {Any*}                    Args       additional args
 * @returns {Boolean}
 * @example
 * Arr := Array(1, 2, 3, 4, 5, 6, 7, 8)
 * 
 * if (Arr.Find(x => x > 4, &Out)) {
 *     MsgBox(Out) ; 5
 * }
 */ 
/**
 * Determines whether the string starts with `Prefix`.
 * `this` `MsgBox()` `ToolTip`
 * @example
 * "Fox".StartsWith("F")       ; true
 * "Fox".StartsWith("f", true) ; false
 * 
 * @param   {String}      Prefix     the given prefix
 * @param   {Primitive?}  CaseSense  case sensitivity options
 * @throws  {UnsetItemError} if the list is empty
 * @returns {Boolean}
 */ 
/**
 * @file
 * @name StringUtils
 * @description
 * Demonstrates how to add custom string utilities.
 */
 ConstantRef(&Value) => { Get: (_) => Value }
 StructField(T, Pack?) => { Type: T, Pack: (Pack?) }
 T.Compare(0) == 0
 "Fox".StartsWith("F")       ; true
 "Fox".StartsWith("f", true) ; false
```